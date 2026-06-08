$body = @{
    prompt = "What is Sewa Setu?"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body -ErrorAction SilentlyContinue

if ($response) {
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Response Type: $($data.response_type)"
    if ($data.response_type -eq "faq") {
        Write-Host "Answer: $($data.answer)"
        Write-Host "Sources: $($data.sources)"
    } elseif ($data.response_type -eq "sql") {
        Write-Host "SQL: $($data.generated_sql)"
        Write-Host "Columns: $($data.columns)"
        Write-Host "Rows: $($data.rows | ConvertTo-Json)"
    }
} else {
    Write-Host "Failed to connect to API"
}
