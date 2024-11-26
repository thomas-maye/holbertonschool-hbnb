INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES 
    ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@mail.com', '$2b$12$3SfkZOeh/cuwctP2kaiEG.6eqyF2g9CTlmbB2oc.YE9h4eBQ8ScVa', TRUE),
    ('1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p', 'Thomas', 'Mayé', 'thomas.maye@mail.com', '$2b$12$3OEAi858s42TSRayvGvvveO04Xy6ehHXA1m3ps9B9lRnOHPrKEe/2', FALSE),
    ('2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', 'Mael', 'Ezanic', 'mael.ezanic@mail.com', '$2b$12$nmNnJ9kL7u934ZNMGzTKY.mtf.cZ58MlcCp3kdeTsZJn/vCQfhCD6', FALSE),
    ('3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', 'Antoine', 'Lafitte', 'antoine.lafitte@mail.com', '$2b$12$4ixPEKOFcpP6g4EZ0.QCuO./qK/oKYlr83wIFHbjt1/xRVvH.DQ3S', FALSE);

INSERT INTO amenities (id, name)
VALUES
    ('2bab839a-28fe-45df-aa93-090cdf1845c0', 'WiFi'),
    ('ed5b4db4-2d19-460b-a44e-58d6d69c0dee', 'Swimming Pool'),
    ('b9774a61-54e5-495e-9040-5c534a8200bc', 'Air Conditioning'),
    ('3c9f8b2a-1d3e-4f6a-9b8d-1e2f3a4b5c6d', 'Gym'),
    ('4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9g', 'Parking'),
    ('5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9g0h', 'Pet Friendly'),
    ('6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9g0h1i', 'Breakfast Included'),
    ('7a8b9c0d-1e2f-3a4b-5c6d-7e8f9g0h1i2j', 'Spa'),
    ('8b9c0d1e-2f3a-4b5c-6d7e-8f9g0h1i2j3k', 'Restaurant');

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES
    ('12345abc-de67-89f0-gh12-ijkl34567890', 'Modern Loft', 'Experience the city life in this modern and stylish loft.', 275.00, 40.7128, -74.0060, '1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p'),
    ('67890def-gh12-34ij-kl56-mnop78901234', 'Rustic Cabin', 'Enjoy a peaceful retreat in this charming rustic cabin.', 320.00, 34.0522, -118.2437, '3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r'),
    ('abcdef12-3456-7890-ghij-klmnopqrstuv', 'Beach House', 'Relax and unwind in this beautiful beach house with ocean views.', 450.00, 36.7783, -119.4179, '2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q'),
    ('ghijkl34-5678-90mn-opqr-stuvwxyzabcd', 'Mountain Retreat', 'Escape to the mountains in this cozy and secluded retreat.', 350.00, 39.7392, -104.9903, '1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p');

INSERT INTO place_amenity (place_id, amenity_id)
VALUES
    ('12345abc-de67-89f0-gh12-ijkl34567890', '2bab839a-28fe-45df-aa93-090cdf1845c0'),
    ('12345abc-de67-89f0-gh12-ijkl34567890', 'ed5b4db4-2d19-460b-a44e-58d6d69c0dee'),
    ('67890def-gh12-34ij-kl56-mnop78901234', 'b9774a61-54e5-495e-9040-5c534a8200bc'),
    ('67890def-gh12-34ij-kl56-mnop78901234', '3c9f8b2a-1d3e-4f6a-9b8d-1e2f3a4b5c6d'),
    ('abcdef12-3456-7890-ghij-klmnopqrstuv', '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9g'),
    ('abcdef12-3456-7890-ghij-klmnopqrstuv', '5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9g0h'),
    ('ghijkl34-5678-90mn-opqr-stuvwxyzabcd', '6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9g0h1i'),
    ('ghijkl34-5678-90mn-opqr-stuvwxyzabcd', '7a8b9c0d-1e2f-3a4b-5c6d-7e8f9g0h1i2j');

INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES
('1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p', 'Amazing place! Very clean and well-located.', 5, '2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', '12345abc-de67-89f0-gh12-ijkl34567890'),
('2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', 'Had a great time, but the WiFi was slow.', 4, '2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q', '67890def-gh12-34ij-kl56-mnop78901234'),
('3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', 'Beautiful location and very comfortable.', 5, '1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p', 'abcdef12-3456-7890-ghij-klmnopqrstuv'),
('4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9g', 'The cabin was cozy but a bit too remote.', 3, '3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', 'ghijkl34-5678-90mn-opqr-stuvwxyzabcd'),
('5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9g0h', 'Loved the beach house! Perfect for a family vacation.', 5, '3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', 'abcdef12-3456-7890-ghij-klmnopqrstuv'),
('6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9g0h1i', 'The loft was modern and stylish, just as described.', 4, '3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r', '12345abc-de67-89f0-gh12-ijkl34567890');