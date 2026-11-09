
$ErrorActionPreference = "Stop"

# ==========================================
# SENTINEL-CORE MASTER AUTOMATION
# ==========================================

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

$RunId = Get-Date -Format "yyyyMMdd_HHmmss_fff"

$Executable = Join-Path $ProjectRoot "cpp_engine\build\sentinel.exe"

$DatasetRelativePath = "cpp_engine/data/sentinel_run_$RunId.csv"
$DatasetPath = Join-Path $ProjectRoot $DatasetRelativePath

$PredictionPath = Join-Path `
    $ProjectRoot `
    "analytics\reports\sentinel_predictions_$RunId.csv"

$PythonScript = Join-Path `
    $ProjectRoot `
    "analytics\scripts\run_inference.py"

# ==========================================
# HELPER: CHECK COMMAND EXIT CODE
# ==========================================

function Check-ExitCode {
    param([string]$Stage)

    if ($LASTEXITCODE -ne 0) {
        throw "$Stage failed with exit code $LASTEXITCODE"
    }
}

try {

    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "       SENTINEL-CORE AUTOMATION" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan

    # ======================================
    # STEP 1: BUILD C++ ENGINE
    # ======================================

    Write-Host ""
    Write-Host "[1/4] Building C++ engine..." -ForegroundColor Yellow

    & cmake --build ".\cpp_engine\build"

    Check-ExitCode "C++ build"

    if (-not (Test-Path $Executable)) {
        throw "C++ executable was not found: $Executable"
    }

    Write-Host "C++ build successful." -ForegroundColor Green

    # ======================================
    # STEP 2: RUN DIGITAL TWIN
    # ======================================

    Write-Host ""
    Write-Host "[2/4] Starting Digital Twin simulation..." -ForegroundColor Yellow

    Write-Host "Dataset: $DatasetRelativePath"
    Write-Host ""
    Write-Host "Operator maintenance prompts may appear."
    Write-Host "Enter a machine ID to authorize maintenance."
    Write-Host "Press Enter to skip maintenance."

    & $Executable $DatasetRelativePath

    Check-ExitCode "Digital Twin simulation"

    if (-not (Test-Path $DatasetPath)) {
        throw "Simulation dataset was not generated."
    }

    Write-Host "Digital Twin simulation completed." -ForegroundColor Green

    # ======================================
    # STEP 3: RUN PYTHON INFERENCE
    # ======================================

    Write-Host ""
    Write-Host "[3/4] Running machine fault inference..." -ForegroundColor Yellow

    & python $PythonScript `
        --input $DatasetPath `
        --output $PredictionPath

    Check-ExitCode "Python inference"

    if (-not (Test-Path $PredictionPath)) {
        throw "Prediction output was not generated."
    }

    Write-Host "Inference completed." -ForegroundColor Green

    # ======================================
    # STEP 4: VALIDATE OUTPUTS
    # ======================================

    Write-Host ""
    Write-Host "[4/4] Validating generated files..." -ForegroundColor Yellow

    $SensorRecords = @(Import-Csv $DatasetPath)
    $PredictionRecords = @(Import-Csv $PredictionPath)

    if ($SensorRecords.Count -eq 0) {
        throw "Sensor dataset is empty."
    }

    if ($SensorRecords.Count -ne $PredictionRecords.Count) {
        throw "Sensor and prediction record counts do not match."
    }

    $RequiredPredictionColumns = @(
        "PredictedFault",
        "Confidence",
        "Prob_NONE",
        "Prob_BEARING_WEAR",
        "Prob_MISALIGNMENT",
        "Prob_COOLING_FAILURE",
        "Prob_OVERLOAD"
    )

    $ActualColumns = $PredictionRecords[0].PSObject.Properties.Name

    foreach ($Column in $RequiredPredictionColumns) {
        if ($Column -notin $ActualColumns) {
            throw "Missing prediction column: $Column"
        }
    }

    $MachineCount = @(
        $SensorRecords.MachineID | Sort-Object -Unique
    ).Count

    Write-Host "Sensor records: $($SensorRecords.Count)"
    Write-Host "Prediction records: $($PredictionRecords.Count)"
    Write-Host "Machines detected: $MachineCount"

    # ======================================
    # FINAL REPORT
    # ======================================

    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "   SENTINEL-CORE PIPELINE SUCCESSFUL" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green

    Write-Host "Run ID: $RunId"
    Write-Host "Dataset: $DatasetPath"
    Write-Host "Predictions: $PredictionPath"

}
catch {

    Write-Host ""
    Write-Host "SENTINEL-CORE PIPELINE FAILED" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red

    exit 1
}
