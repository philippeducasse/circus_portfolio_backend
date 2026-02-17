<?php
require "db.php";

$db->exec("
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        show TEXT,
        message TEXT NOT NULL,
        date TEXT NOT NULL
    )
");

echo "Comments table created successfully";
