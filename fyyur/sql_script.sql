

INSERT INTO venue (id, name, genres, address, city, state, phone, website_link,
 facebook_link, seeking_talent, seeking_description, image_link)
 values (1, 'The Musical Hop', 'Jazz, Reggae, Swing, Classical, Folk',
  '1015 Folsom Street', 'GHUDAF', 'CA','000-000-0000',
    'https://www.themusicalhop.com', 'https://www.facebook.com/TheMusicalHop',
     'True',  '#DESC#',
      'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60');





INSERT INTO venue (id, name, genres, address, city, state, phone, website_link,
 facebook_link, seeking_talent, seeking_description, image_link)
 values (2, 'The Dueling Pianos Bar', 'Classical", "R&B", "Hip-Hop',
  '335 Delancey Street', 'GHUDAF', 'NY','000-000-0000',
    'https://www.theduelingpianos.com', 'https://www.facebook.com/theduelingpianos',
     'False',  '#DESC#',
      'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80');






INSERT INTO venue (id, name, genres, address, city, state, phone, website_link,
 facebook_link, seeking_talent, seeking_description, image_link)
 values (3, 'Park Square Live Music & Coffee', 'Rock n Roll, Jazz, Classical, Folk',
  '34 Whiskey Moore Ave', 'GHUDAF', 'CA','000-000-0000',
    'ttps://www.parksquarelivemusicandcoffee.com', 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
     'False',  '#DESC#',
      'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80');

INSERT INTO artist (id, name, genres, city, state, phone, website_link, facebook_link, looking_for_venues, seeking_description, image_link)
values (4,'Guns N Petals', 'Rock n Roll', 'GHUDAF','CA','000-000-0000',
'https://www.gunsnpetalsband.com','https://www.facebook.com/GunsNPetals',
'True', '#DESCRIPTION#', 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80' );


INSERT INTO artist (id, name, genres, city, state, phone , facebook_link, looking_for_venues, seeking_description, image_link)
values (5,'Matt Quevedo', 'Jazz', 'GHUDAF','NY','000-000-0000'
,'https://www.facebook.com/mattquevedo923251523',
'True', '#DESCRIPTION#', 'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80' );

INSERT INTO artist (id, name, genres, city, state, phone, website_link, facebook_link, looking_for_venues, seeking_description, image_link)
values (6,'The Wild Sax Band', '"Jazz, "Classical', 'GHUDAF','CA','000-000-0000',
'https://www.gunsnpetalsband.com','https://www.facebook.com/GunsNPetals',
'False', '#DESCRIPTION#', 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80' );


INSERT INTO show (artist_id, venue_id, start_time) values (4, 1, '2019-05-21T21:30:00.000Z');
INSERT INTO show (artist_id, venue_id, start_time) values (5, 3, '2019-06-15T23:00:00.000Z');
INSERT INTO show (artist_id, venue_id, start_time) values (6, 3, '2035-04-01T20:00:00.000Z');
INSERT INTO show (artist_id, venue_id, start_time) values (6, 3, '2035-04-08T20:00:00.000Z');
INSERT INTO show (artist_id, venue_id, start_time) values (6, 3, '2035-04-15T20:00:00.000Z');