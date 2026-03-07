<?php
require "db.php";

try {
    $db->exec("
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        organisation TEXT,
        project_id INTEGER,
        message TEXT NOT NULL,
        message_en TEXT,
        message_fr TEXT,
        sentiment TEXT,
        date TEXT NOT NULL
    )
");
} catch (PDOException $e) {
    echo "Error creating projects table: " . $e->getMessage();
}

echo "Reviews table created successfully";
