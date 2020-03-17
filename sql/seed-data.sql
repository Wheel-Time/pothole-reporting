INSERT INTO site_user (username, first_name, last_name, email, pword, is_admin)
VALUES
('isaac', 'Isaac', 'Poulin', 'ipoulin@unomaha.edu', 'pass1', true),
('bishwo', 'Bishwo', 'Karki', 'bishwokarki@unomaha.edu', 'pass2', true),
('ethan', 'Ethan', 'Triplett', 'emtriplett@unomaha.edu', 'pass3', true),
('frankie', 'Frankie', 'Holzapfel', 'fholzapfel@unomaha.edu', 'pass4', true);

INSERT INTO pothole (pothole_point)
VALUES (POINT(0,0));

-- pothole reports
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 1, 5);
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 2, 5);
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 3, 5);
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 4, 5);
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 1, 5);
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 2, 5);

-- fixed reports
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 1, 0);
INSERT INTO pothole_ledger (fk_pothole_id, fk_user_id, state)
VALUES (1, 2, 0);