#!/usr/bin/env bash

VENV_DIR=".venv"

# 1️⃣ Create / activate virtual environment
if [ -d "$VENV_DIR" ]; then
    echo "✅ Virtual environment already exists in $VENV_DIR"
    echo "👉 Activating it..."
else
    echo "🚀 Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate
source "$VENV_DIR/bin/activate"

# 1️⃣a Add LocalStack dummy credentials automatically
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1

# 2️⃣ Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# 3️⃣ Install Python dependencies
echo "📥 Installing dependencies..."
pip install boto3 localstack pyspark python-dotenv

# 4️⃣ Check Docker
if ! command -v docker >/dev/null 2>&1; then
    echo "⚠️ Docker not found. LocalStack requires Docker."
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    echo "Exiting setup."
    exit 1
else
    echo "🐳 Docker found!"
fi

# 5️⃣ Start LocalStack safely
echo ""
echo "🚀 Starting LocalStack..."
if localstack status | grep -q "running"; then
    echo "ℹ️ LocalStack is already running."
else
    localstack start &
    echo "⏳ Waiting a few seconds for LocalStack to start..."
    sleep 5
fi

# 6️⃣ Instructions
echo ""
echo "🎉 Setup complete!"
echo "👉 To deactivate the environment: deactivate"
echo "👉 Current Python: $(which python)"
echo "👉 Current Pip:    $(which pip)"
echo ""
echo "💡 LocalStack is now running in the background."
echo "💡 Example: Run a script against LocalStack:"
echo "   python s3/s3.py"
echo ""
echo "💡 Dummy AWS credentials have been set automatically:"
echo "   AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID"
echo "   AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"
echo "   AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION"
