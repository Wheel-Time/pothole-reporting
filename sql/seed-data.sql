INSERT INTO site_user (username, first_name, last_name, email, pass, is_admin)
VALUES
('isaac', 'Isaac', 'Poulin', 'ipoulin@unomaha.edu', 'pass1', true),
('bishwo', 'Bishwo', 'Karki', 'bishwokarki@unomaha.edu', 'pass2', true),
('ethan', 'Ethan', 'Triplett', 'emtriplett@unomaha.edu', 'pass3', true),
('frankie', 'Frankie', 'Holzapfel', 'fholzapfel@unomaha.edu', 'pass4', true);

INSERT INTO pothole (pothole_point)
VALUES (POINT(0,0));

INSERT INTO pothole_ledger (pothole__id, user__id, state)
VALUES (LAST_INSERT_ID(), 1, 5);