INSERT INTO site_user (username, first_name, last_name, email, pword, is_admin)
VALUES
('isaac', 'Isaac', 'Poulin', 'ipoulin@unomaha.edu', 'pass1', true),
('bishwo', 'Bishwo', 'Karki', 'bishwokarki@unomaha.edu', 'pass2', true),
('ethan', 'Ethan', 'Triplett', 'emtriplett@unomaha.edu', 'pass3', true),
('frankie', 'Frankie', 'Holzapfel', 'fholzapfel@unomaha.edu', 'pass4', true);

INSERT INTO pothole (lat, lon)
VALUES
    (41.250715, -96.011354),
    (41.251925, -96.008073),
    (41.252781, -96.010922),
    (41.248748, -96.019297),
    (41.259516, -96.023746),
    (41.243736, -96.013085);

-- pothole reports
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES
    (1, 1, 5), (1, 2, 5), (1, 3, 5), (1, 4, 5), (1, 1, 5), (1, 2, 5),
    (2, 1, 3), (2, 2, 3), (2, 3, 3), (2, 4, 3), (2, 1, 3), (2, 2, 3), (2, 3, 3), (2, 4, 3),
    (3, 1, 4), (3, 2, 4), (3, 3, 4), (3, 4, 4), (3, 1, 4),
    (4, 1, 1), (4, 2, 1), (4, 3, 1), (4, 4, 1), (4, 1, 1), (4, 2, 1), (4, 3, 1),
    (5, 1, 5), (5, 2, 5), (5, 3, 5), (5, 4, 5), (5, 1, 5), (5, 2, 5),
    (6, 1, 4), (6, 2, 4), (6, 3, 4), (6, 4, 4), (6, 1, 4), (6, 2, 4);


-- fixed reports
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES
    (1, 1, 0), (1, 2, 0),
    (5, 3, 0);
