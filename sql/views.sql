DROP VIEW IF EXISTS vw_pothole;
CREATE VIEW vw_pothole AS
SELECT
		p.id,
        p.lat,
        p.lon,
        p.create_date,
        CASE -- need to add admin check
			WHEN SUM(CASE
				WHEN pl.state > 0
                THEN 1
                ELSE 0
			END) >= 5 -- reports until confirm
            THEN MIN(CASE
				WHEN pl.state > 0
                THEN pl.submit_date
                ELSE '9999-12-31 23:59:59'
			END)
            ELSE NULL
		END AS 'effective_date',
		CASE -- need to add admin check
			WHEN SUM(CASE
				WHEN pl.state = 0
                THEN 1
                ELSE 0
			END) > 5 -- reports until confirm
            THEN MIN(CASE
				WHEN pl.state = 0
                THEN pl.submit_date
                ELSE '9999-12-31 23:59:59'
			END)
            ELSE '9999-12-31 23:59:59'
		END AS 'fixed_date',
        SUM(CASE WHEN pl.state > 0 THEN 1 ELSE 0 END) AS 'pothole_reports',
        SUM(CASE WHEN pl.state = 0 THEN 1 ELSE 0 END) AS 'fixed_reports',
        AVG(CASE WHEN pl.state > 0 THEN pl.state ELSE null END) AS 'avg_severity'
	FROM pothole_reporting.pothole p
		LEFT JOIN pothole_reporting.pothole_ledger pl ON pl.fk_pothole_id = p.id
	GROUP BY p.id, p.lat, p.lon, p.create_date;

SELECT * FROM pothole_reporting.vw_pothole