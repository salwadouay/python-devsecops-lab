pipeline {
    agent any
    environment {
        // Set up Python and Docker
        PYTHON_IMAGE = 'python:3.9-slim'
        // IMAGE_NAME is used for tagging the Docker image
        IMAGE_NAME = 'python-devsecops-jenkins_app'
    }
    stages {
        stage('Checkout') {
            steps {
                // Pull the code from GitHub
                checkout scm
            }
        }

        stage('Install All Dependencies & Tools') {
            steps {
                script {
                    // 1. Create Virtual Environment
                    sh 'python3 -m venv venv'
                    
                    // 2. Install APPLICATION dependencies (Flask) and Pytest
                    // NOTE: requirements.txt MUST include pytest
                    sh './venv/bin/pip install -r requirements.txt'
                    
                    // 3. Install DEVSECOPS tools (Bandit, Safety) into the VENV
                    sh './venv/bin/pip install bandit safety'
                }
            }
        }

        stage('Run Tests') {
            // Run the tests with pytest
            steps {
                sh './venv/bin/pytest'
            }
        }

        stage('Static Code Analysis (Bandit)') {
            // Scan source code for security flaws (hardcoded secrets, etc.)
            steps {
                sh './venv/bin/bandit -r .'
            }
        }

        stage('Check Dependency Vulnerabilities (Safety)') {
            // Check application dependencies against known CVEs
            steps {
                // Using the recommended 'scan' command instead of deprecated 'check'
                sh './venv/bin/safety scan --full-report -r requirements.txt'
            }
        }

        stage('Build & Scan Docker Image (Trivy)') {
            steps {
                script {
                    // 1. Build the Docker image explicitly with a tag
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                    
                    // 2. Scan the built image for OS and package vulnerabilities
                    sh "trivy image ${IMAGE_NAME}:latest"
                }
            }
        }
        
        // Push Docker Image stage is assumed here if you are deploying to a registry

        stage('Deploy Application') {
            // Deploy the application using Docker Compose
            steps {
                sh 'docker-compose up -d' 
            }
        }
    }
    post {
        always {
            // Clean up the workspace files after the build completes
            cleanWs()
        }
    }
}
