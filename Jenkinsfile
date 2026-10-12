
pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests with pytest') {
            steps {
                echo 'Running Selenium Tests using pytest'

                bat 'start /B python app.py'

                bat 'ping 127.0.0.1 -n 6 > nul'

                bat 'python -m pytest test/test_registration.py -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Build Docker Image'
                bat 'docker build -t kubdemoapp:v1 .'
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    bat 'docker login -u %DOCKER_USERNAME% -p %DOCKER_PASSWORD%'
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo 'Pushing Docker Image to Docker Hub'

                bat 'docker tag kubdemoapp:v1 dayalaharimya/week8:kubeimage1'

                bat 'docker push dayalaharimya/week8:kubeimage1'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying application to Kubernetes'

                bat 'kubectl apply -f deployment.yaml --validate=false'

                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Please check the logs.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
