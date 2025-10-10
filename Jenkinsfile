pipeline {
    agent any

    environment {
        PYTHON = "/usr/bin/python3"
        PIP = "/usr/bin/pip3"
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = "yourdockerhubusername/flask-app"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing dependencies...'
                sh '''
                    ${PIP} install --upgrade pip
                    ${PIP} install -r requirements.txt || ${PIP} install Flask pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running pytest...'
                sh '''
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo '📦 Pushing image to Docker Hub...'
                sh '''
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD pipeline completed successfully!'
        }
        failure {
            echo '❌ Build or tests failed!'
        }
    }
}
