<?php
require "db/db.php";

$allowed_origins = ["http://localhost:3000", "https://philippeducasse.com", "http://127.0.0.1:3000"];
$origin = $_SERVER["HTTP_ORIGIN"] ?? "";

if (in_array($origin, $allowed_origins)) {
    header("Access-Control-Allow-Origin: $origin");
}
header("Content-Type: application/json");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

$method = $_SERVER["REQUEST_METHOD"];

if ($method === "POST") {
    try {
        $data = json_decode(file_get_contents("php://input"), true);

        if (!$data) {
            echo json_encode(["error" => "Invalid JSON"]);
            exit;
        }

        $review = [
            "name" => $data["name"] ?? "Anonymous",
            "project_id" => $data["project_id"] ?? null,
            "message" => $data["message"],
            "organisation" => $data["organisation"] ?? null,
            "date" => date("d-m-y H:i:s")
        ];

        // SQL prepare statement protects against SQL injection attacks
        $stmt = $db->prepare("INSERT INTO reviews (name, project_id, message, date, organisation) VALUES (:name, :project_id, :message, :date, :organisation)");
        $stmt->execute($review);


        echo json_encode(["success" => true, "id" => $db->lastInsertId()]);
    } catch (Exception $e) {
        http_response_code(400);
        echo json_encode(["error" => $e->getMessage()]);
    }
}
if ($method === "GET") {
    $stmt = $db->prepare("SELECT * FROM reviews ORDER BY date DESC");
    $stmt->execute();
    // returns associative arrays instead of objects. They are simpler and JSON encode handles them naturally
    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
} else {
    echo json_encode(["success" => false]);
}
