# Назначение
Программа предназначена для выявления оборудования, подвергшегося несанкционированной эксплуатации (самозахвату).

# Описание программы
Программа представляет собой исполняемый exe-файл, предназначенный для запуска в OS Windows.
Взаимодействие с программой осуществляется через графический интерфейс (**далее GUI**):
![alt text](docs/for_README.md_1.png)
Программа принимает исходные данные в виде таблицы Эксель, к которой добавляет признаки, по которым можно выявить самовольно захваченное оборудование. Результат выгружается в Эксель-файл.
**Для того чтобы программа работала, пользователю нужно подключиться к базе данных в DWH (например к БД audit) с грантом позволяющим создавать таблицы.**
Подключение к базе данных осуществляется через GUI.
GUI позволяет пользователю "залогиниться", "разлогиниться" (при этом данные о параметрах подключения будут удалены с машины пользователя) или, при необходимости, поменять параметры подключения. 
**Параметры подключения хранятся только на машине пользователя, причём в зашифрованном виде.**

GUI позоволяет выбрать исходную книгу эксель в файловой системе локальной машины и лист этой книги содержащей исходные данные.
Заголовки таблицы могут находится не в первой строке листа. Интерфейс позволяет "поднять" или "опустить" таблицу, чтобы заголовки оказались в перовй строке.
Так же можно открыть исходный файл с помощью интерфейса, чтобы облегчить поиск его в файловой системе, если этот файл нужно откорректировать.
**После изменения и сохранения изменений в исходном файле его следуте заново загрузить в программу!!!**

# Ограничения
Программа тестировалась на машине с 16Гб оперативной памяти на исходном файле содержащем 750 тысяч строк.
На выборке 1 млн.строк. программа выдала сообщение об ошибке, так как на локальной машине не хватило памяти для выгрузки датафрейма с результатом в Эксель-файл.
На практике размер таблицы из загружаемого в программу экслевского файла не превышает 10000 строк. Вероятность того, что потребуется загружать таблицы с большим количеством строк минимальна.

# Описание алгоритма
Программа принимает на вход экселевский файл, с таблицей, которая должна содержать обязательные поля:
- Ст. Отправления
- Ст. Назначения
- № Вагона
- № контейнера
- Тип контейнера
- № накладной
- Наименование груза
- Дата отправки

Данные из экселевского файла загружаются в датафрейм на основании которого в тестовом контуре Clickhouse создаётся таблица **audit.tmp_unauthorized_seizure** с полями:
- \`Ст. Отправления\`
- \`Ст. Назначения\`
- \`№ Вагона\`
- \`№ контейнера\`
- \`№ контейнера (проверенный)\`
- \`Тип контейнера\`
- \`№ накладной\`
- \`Наименование груза\`
- \`Дата отправки\`
- \`Дата отправки (проверенная)\`

Поле \`№ контейнера (проверенный)\` содержит значение из поля \`№ контейнера\`, если это поле содержит строку длиной 11 символов, из которых первые 4 символа - латиница в верхнем регистре и 7 последних - цифры. В противном случае поле \`№ контейнера (проверенный)\` имеет значение Null.

Поле \`Дата отправки (проверенная)\` содержат значение из поля \`Дата отправки\` если это значение может быть распознано как дата, и Null - если не может.

Далее в тестовом контуре Clickhouse выполняется запрос с использованием таблиц **audit.tmp_unauthorized_seizure** и **history.rks__directly**.

**SQL-запрос написан с учетом особенностей работы с большими таблицами в Clickhouse, выполняется быстро и с минимальной нагрузкой на БД.**

```
/*******************************************************************************************/
/*  В коде запроса закомментированы строки нужные для поэтапной отладки в случае "поломки" */
/*******************************************************************************************/
WITH 
	SVOD AS (
		SELECT 
			`Ст. Отправления`,
			`Ст. Назначения`,
			`№ Вагона`,
			`№ контейнера`,
			`№ контейнера (проверенный)`,
			`Тип контейнера`,
			`№ накладной`,
			`Наименование груза`,
			`Дата отправки`,
			`Дата отправки (проверенная)`,
			'' AS `Дата прибытия`
		FROM 
			audit.tmp_unauthorized_seizure
--) SELECT * FROM SVOD
	),
	RKS_RZD AS ( 
		SELECT
			`document_reasons_number`,
			anyIf(`document_reasons_number`, `esu_id` = '0.02.01.01') OVER (PARTITION BY `container_number`, `Date_E`) AS `document_reasons_number_0.02.01.01`,
			IF (`document_reasons_number` = '', `document_reasons_number_0.02.01.01`, `document_reasons_number`) AS document_reasons_number_processed,
			`service_details_order_id` AS order_id,
			replace(replace(replace(upperUTF8(service_details_container_number),' ',''),'Т','T'),'К','K')  AS container_number,
			esu_id,
			min(date_end) AS `Date_E`,
			sum(amount_in_rub_without_vat) AS `amount_in_rub_without_vat_sum`,
			sum(amount_in_contract_currency_without_vat) AS `amount_in_contract_currency_without_vat_sum`		
		FROM 
			history.rks__directly
		WHERE
			container_number IN (SELECT DISTINCT`№ контейнера (проверенный)` FROM SVOD WHERE  `№ контейнера (проверенный)`<>'')	AND	
			esu_id IN ('0.01.01.01', '0.01.01.02', '0.01.01.04', '2.01.01.01', '0.02.01.01') AND
			document_reasons_number <> ''
		GROUP BY 
			document_reasons_number,
			order_id,
			container_number,
			esu_id
		HAVING
			`amount_in_rub_without_vat_sum` <> 0 OR 
			`amount_in_contract_currency_without_vat_sum` <> 0 
--) SELECT * FROM RKS_RZD WHERE container_number = 'TKRU3539156'					
),
	RKS_RZD AS (
		SELECT
			document_reasons_number_processed,
			container_number,
			sumIf(amount_in_rub_without_vat_sum              , esu_id = '0.01.01.01') AS `amount_in_rub_without_vat_sum_0.01.01.01`,
			sumIf(amount_in_contract_currency_without_vat_sum, esu_id = '0.01.01.01') AS `amount_in_contract_currency_without_vat_sum_0.01.01.01`,
			sumIf(amount_in_rub_without_vat_sum              , esu_id = '0.01.01.02') AS `amount_in_rub_without_vat_sum_0.01.01.02`,
			sumIf(amount_in_contract_currency_without_vat_sum, esu_id = '0.01.01.02') AS `amount_in_contract_currency_without_vat_sum_0.01.01.02`,
			sumIf(amount_in_rub_without_vat_sum              , esu_id = '0.01.01.04') AS `amount_in_rub_without_vat_sum_0.01.01.04`,
			sumIf(amount_in_contract_currency_without_vat_sum, esu_id = '0.01.01.04') AS `amount_in_contract_currency_without_vat_sum_0.01.01.04`,
			sumIf(amount_in_rub_without_vat_sum              , esu_id = '2.01.01.01') AS `amount_in_rub_without_vat_sum_2.01.01.01`,
			sumIf(amount_in_contract_currency_without_vat_sum, esu_id = '2.01.01.01') AS `amount_in_contract_currency_without_vat_sum_2.01.01.01`
		FROM
			RKS_RZD
		GROUP BY 
			document_reasons_number_processed,
			container_number
		HAVING 
			`amount_in_rub_without_vat_sum_0.01.01.01` <> 0                 OR 
			`amount_in_contract_currency_without_vat_sum_0.01.01.01` <> 0   OR
			`amount_in_rub_without_vat_sum_0.01.01.02` <> 0                 OR 
			`amount_in_contract_currency_without_vat_sum_0.01.01.02` <> 0   OR
			`amount_in_rub_without_vat_sum_0.01.01.04` <> 0                 OR 
			`amount_in_contract_currency_without_vat_sum_0.01.01.04` <> 0   OR	
			`amount_in_rub_without_vat_sum_2.01.01.01` <> 0                 OR 
			`amount_in_contract_currency_without_vat_sum_2.01.01.01` <> 0   
--) SELECT * FROM RKS_RZD WHERE container_number = 'TKRU3539156'
),	
	RKS AS (
		SELECT 
			service_details_order_id AS order_id,
			replace(replace(replace(upperUTF8(service_details_container_number),' ',''),'Т','T'),'К','K') AS container_number,
			DC.name AS client_name, 
			DL_FROM.name AS points_from_catalog_name,	
			DL_TO.name AS points_to_catalog_name,
			DSt_FROM.station_name AS station_name_from,		
			DSt_TO.station_name AS station_name_to,		
			DSe.name AS service_name,
			min(date_end) AS `Date_E`,
			sum(amount_in_rub_without_vat) AS `amount_in_rub_without_vat_sum`,
			sum(amount_in_contract_currency_without_vat) AS `amount_in_contract_currency_without_vat_sum`		
		FROM 
			history.rks__directly               AS RD
			INNER JOIN (SELECT DISTINCT `№ контейнера (проверенный)`, `Дата отправки (проверенная)` FROM SVOD WHERE  `№ контейнера (проверенный)`<>'') AS SVOD ON SVOD.`№ контейнера (проверенный)` = container_number			
			LEFT JOIN history.dict_counterparty AS DC       ON RD.client_number_id = DC.id
			LEFT JOIN history.dict_service      AS DSe      ON RD.esu_id = DSe.id 
			LEFT JOIN history.dict_location     AS DL_FROM  ON RD.service_details_points_from_catalog_id = DL_FROM.id
			LEFT JOIN history.dict_location     AS DL_TO    ON RD.service_details_points_to_catalog_id = DL_TO.id
			LEFT JOIN history.dict_stations     AS DSt_FROM ON RD.service_details_points_from_station_id = DSt_FROM.station_code
			LEFT JOIN history.dict_stations     AS DSt_TO   ON RD.service_details_points_to_station_id = DSt_TO.station_code
		WHERE
			esu_id IN ('0.01.01.01', '0.01.01.02', '0.01.01.04', '2.01.01.01')
		GROUP BY 
			order_id,
			container_number,	
			client_name,
			DL_FROM.name,
			DL_TO.name,
			service_name,
			station_name_from,	
			station_name_to		
		HAVING
			`amount_in_rub_without_vat_sum` <> 0 OR 
			`amount_in_contract_currency_without_vat_sum` <> 0			
--) SELECT * FROM RKS
),
	RKS_BEFORE AS ( 	
		SELECT
			 SVOD.`№ контейнера (проверенный)` AS `№ контейнера (проверенный)`, SVOD.`Дата отправки (проверенная)` AS `Дата отправки (проверенная)`,
			--order_id,container_number,client_name,points_from_catalog_name,points_to_catalog_name,station_name_from,station_name_to,service_name,Date_E,amount_in_rub_without_vat_sum,amount_in_contract_currency_without_vat_sum
			IF(`Date_E` = '1970-01-01 03:00:00', Null, date_diff( DAY, SVOD.`Дата отправки (проверенная)`, `Date_E`)) AS date_diff,
			argMaxIf(`order_id`                                   , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `order_id`,
			argMaxIf(`client_name`                                , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `client_name`,
			argMaxIf(`points_from_catalog_name`                   , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `points_from_catalog_name`,
			argMaxIf(`points_to_catalog_name`                    , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `points_to_catalog_name`,
			argMaxIf(`station_name_from`                          , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `station_name_from`,
			argMaxIf(`station_name_to`                            , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `station_name_to`,
			argMaxIf(`service_name`                               , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `service_name`,
			argMaxIf(`Date_E`                                     , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `Date_E`,
			argMaxIf(`amount_in_rub_without_vat_sum`              , RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `amount_in_rub_without_vat_sum`,
			argMaxIf(`amount_in_contract_currency_without_vat_sum`, RKS.`Date_E`, RKS.`Date_E` <= SVOD.`Дата отправки (проверенная)`) AS `amount_in_contract_currency_without_vat_sum`
		FROM
			RKS
			INNER JOIN (SELECT DISTINCT `№ контейнера (проверенный)`, `Дата отправки (проверенная)` FROM SVOD WHERE `№ контейнера (проверенный)`<>'') AS SVOD ON SVOD.`№ контейнера (проверенный)` = RKS.container_number
		GROUP BY
			SVOD.`№ контейнера (проверенный)`,
			SVOD.`Дата отправки (проверенная)`
--) SELECT * FROM RKS_BEFORE
	),	
	RKS_AFTER AS ( 
		SELECT
			 SVOD.`№ контейнера (проверенный)` AS `№ контейнера (проверенный)`, SVOD.`Дата отправки (проверенная)` AS `Дата отправки (проверенная)`,
			--order_id,container_number,client_name,points_from_catalog_name,points_to_catalog_name,station_name_from,station_name_to,service_name,Date_E,amount_in_rub_without_vat_sum,amount_in_contract_currency_without_vat_sum
			IF(`Date_E` = '1970-01-01 03:00:00', Null, date_diff( DAY, SVOD.`Дата отправки (проверенная)`, `Date_E`)) AS date_diff,
			argMinIf(`order_id`                                   , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `order_id`,
			argMinIf(`client_name`                                , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `client_name`,
			argMinIf(`points_from_catalog_name`                   , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `points_from_catalog_name`,
			argMinIf(`points_to_catalog_name`                    , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `points_to_catalog_name`,
			argMinIf(`station_name_from`                          , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `station_name_from`,
			argMinIf(`station_name_to`                            , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `station_name_to`,
			argMinIf(`service_name`                               , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `service_name`,
			argMinIf(`Date_E`                                     , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `Date_E`,
			argMinIf(`amount_in_rub_without_vat_sum`              , RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `amount_in_rub_without_vat_sum`,
			argMinIf(`amount_in_contract_currency_without_vat_sum`, RKS.`Date_E`, RKS.`Date_E` >= SVOD.`Дата отправки (проверенная)`) AS `amount_in_contract_currency_without_vat_sum`
		FROM
			RKS
			INNER JOIN (SELECT DISTINCT `№ контейнера (проверенный)`, `Дата отправки (проверенная)` FROM SVOD WHERE  `№ контейнера (проверенный)`<>'') AS SVOD ON SVOD.`№ контейнера (проверенный)` = RKS.container_number
		GROUP BY
			SVOD.`№ контейнера (проверенный)`,
			SVOD.`Дата отправки (проверенная)`
--) SELECT * FROM RKS_AFTER				
)
SELECT
	count() OVER() AS `всего строк`,
	SVOD.`Ст. Отправления` ,SVOD.`Ст. Назначения`,SVOD.`№ Вагона`,SVOD.`№ контейнера`,SVOD.`№ контейнера (проверенный)`,SVOD.`Тип контейнера`,SVOD.`№ накладной`,SVOD.`Наименование груза`,SVOD.`Дата отправки`,SVOD.`Дата отправки (проверенная)`,SVOD.`Дата прибытия`,
	RKS_RZD.`document_reasons_number_processed`,--RKS_RZD.`container_number`,
	RKS_RZD.`amount_in_rub_without_vat_sum_0.01.01.01`,RKS_RZD.`amount_in_contract_currency_without_vat_sum_0.01.01.01`,RKS_RZD.`amount_in_rub_without_vat_sum_0.01.01.02`,RKS_RZD.`amount_in_contract_currency_without_vat_sum_0.01.01.02`,RKS_RZD.`amount_in_rub_without_vat_sum_0.01.01.04`,RKS_RZD.`amount_in_contract_currency_without_vat_sum_0.01.01.04`,RKS_RZD.`amount_in_rub_without_vat_sum_2.01.01.01`,RKS_RZD.`amount_in_contract_currency_without_vat_sum_2.01.01.01`,
	--RKS_BEFORE.`№ контейнера (проверенный)`,RKS_BEFORE.`Дата отправки (проверенная)`,
	RKS_BEFORE.`date_diff`,RKS_BEFORE.`Date_E`,RKS_BEFORE.`order_id`,RKS_BEFORE.`client_name`,RKS_BEFORE.`points_from_catalog_name`,RKS_BEFORE.`points_to_catalog_name`,RKS_BEFORE.`station_name_from`,RKS_BEFORE.`station_name_to`,RKS_BEFORE.`service_name`,RKS_BEFORE.`amount_in_rub_without_vat_sum`,RKS_BEFORE.`amount_in_contract_currency_without_vat_sum`,
	--RKS_AFTER.`№ контейнера (проверенный)`,RKS_AFTER.`Дата отправки (проверенная)`,
	RKS_AFTER.`date_diff`,RKS_AFTER.`Date_E`,RKS_AFTER.`order_id`,RKS_AFTER.`client_name`,RKS_AFTER.`points_from_catalog_name`,RKS_AFTER.`points_to_catalog_name`,RKS_AFTER.`station_name_from`,RKS_AFTER.`station_name_to`,RKS_AFTER.`service_name`,RKS_AFTER.`amount_in_rub_without_vat_sum`,RKS_AFTER.`amount_in_contract_currency_without_vat_sum`
FROM 
	SVOD
	LEFT JOIN RKS_RZD ON SVOD.`№ контейнера (проверенный)` = RKS_RZD.container_number AND SVOD.`№ накладной` = RKS_RZD.document_reasons_number_processed
	LEFT JOIN RKS_BEFORE AS RKS_BEFORE ON SVOD.`№ контейнера (проверенный)`  = RKS_BEFORE.`№ контейнера (проверенный)` AND SVOD.`Дата отправки (проверенная)` = RKS_BEFORE.`Дата отправки (проверенная)`	 		
	LEFT JOIN RKS_AFTER AS RKS_AFTER ON SVOD.`№ контейнера (проверенный)`  = RKS_AFTER.`№ контейнера (проверенный)`	AND SVOD.`Дата отправки (проверенная)`  = RKS_AFTER.`Дата отправки (проверенная)`	 
```

Перед запуском SQL-запроса пользователь получает уведомление через интерфейс о ячейках в исходном Эксель-файле с некорреткными значениями в полях \`№ контейнера\` и \`Дата отправки\`.
Пользователь может исправить исходные данные или запуситиь SQL-запрос на тех данных, что есть.

Выгрузка результата возможна для исходника с некорреткными значениями в полях \`№ контейнера\` и \`Дата отправки\`, но результат будет подтянут только для строк с правильными значениями.некорреткными значениями в полях \`№ контейнера\` и \`Дата отправки\`.

После выполнения запроса таблица **audit.tmp_unauthorized_seizure** удаляется из Clickhouse.

Результат запроса выгружается в датафрейм из которого, в свою очередь выгружается в Эксель-файл, который сохраняется в локальной папке **Downloads**.



# Инструкция по созданию исполняемого файла

* Скопируйте проект из репозитория на локальный компьютер с предустановленным >=Python3.10<=Python3.12 (на 2025-02-09 для python3.13 библотеки загруженные через pip "отказывались" работать и требовали обнавления некоторых компонентов Windows)
* Перейдите в папку проекта
```cd ~\...\unauthorized_seizure```

* Создайте виртуальное окружение
```python -m venv .venv```

* Активируйте виртуальное окружение
```.venv/Scrits/activate```

* Установите зависимости
```pip install -r requirements.txt```

* Запустите auto-py-to-exe 
```auto-py-to-exe```
Выберите файл unauthorirized_seizure.py,
задайте параметры "One File", "Window DBased (hide hte console)"
Нажмите "CONVERT .PY TO .EXE".

Исполняемый файл появится во вложенной папке ~\...\unauthorized_seizure\output\unauthorized_seizure.exe
