WITH 
	SVOD AS (
		SELECT * FROM audit.cvetkov_d_LOADED_noyabr_2024_xlsx_ktk
--) SELECT *FROM SVOD
	),
	SVOD AS (
		SELECT 
			`Ст. Отправления`,
			`Ст. Назначения`,
			`№ Вагона`,
			`№ контейнера`,
			`№ контейнера` `№ контейнера (проверенный)`,
			`Тип контейнера`,
			`№ накладной`,
			`Наименование груза`,
			`Дата отправки`,
			`Дата отправки` `Дата отправки (проверенная)`,
			'' AS `Дата прибытия`
		FROM 
			SVOD
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

		
