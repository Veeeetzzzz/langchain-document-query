# Check if Python is installed
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Host "Please install Python from https://www.python.org/downloads/ and then re-run the script."
    exit
}

# Check if winget is installed
$winget = Get-Command winget -ErrorAction SilentlyContinue

if (-not $winget) {
    Write-Host "Please install winget (Windows Package Manager) from https://github.com/microsoft/winget-cli/releases and then re-run the script."
    exit
}

# Check if Git is installed, if not, install it
$git = Get-Command git -ErrorAction SilentlyContinue

if (-not $git) {
    Write-Host "Installing Git..."
    winget install --id Git.Git -e --source winget
}

# Clone the NoMoreSQL repository
Write-Host "Cloning NoMoreSQL repository..."
git clone https://github.com/Veeeetzzzz/NoMoreSQL.git

# Change directory
Set-Location -Path NoMoreSQL

# Install requirements
Write-Host "Installing requirements..."
pip install -r requirements.txt

# Set the OpenAI API key as an environment variable
$apiKey = Read-Host -Prompt "Please enter your OpenAI API key"
[System.Environment]::SetEnvironmentVariable("OPEN_API_KEY", $apiKey, "User")

Write-Host "Installation complete."
