SELECT setval('age_restriction_id_seq', max(id)) FROM age_restriction;
SELECT setval('country_id_seq', max(id)) FROM country;
SELECT setval('director_id_seq', max(id)) FROM director;
SELECT setval('genre_id_seq', max(id)) FROM genre;
SELECT setval('user_id_seq', max(id)) FROM "user";
SELECT setval('movie_id_seq', max(id)) FROM movie;
