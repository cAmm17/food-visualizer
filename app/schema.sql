DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS food;
DROP TABLE IF EXISTS user_saved_portions;
DROP TABLE IF EXISTS foods_in_portion;

CREATE TABLE food (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  food_name TEXT UNIQUE NOT NULL,
  model_path TEXT NOT NULL,
  calories INT NOT NULL,
  carbohydrates REAL NOT NULL,
  sugar REAL NOT NULL,
  fat REAL NOT NULL,
  saturated_fat REAL NOT NULL,
  protein REAL NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_saved_portions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  notes TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


CREATE TABLE foods_in_portion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INT NOT NULL,
    portion_id INT NOT NULL,
    amount INT NOT NULL,
    FOREIGN KEY (food_id) REFERENCES food (id),
    FOREIGN KEY (portion_id) REFERENCES user_saved_portions (id)
);
