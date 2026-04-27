pipeline {
    agent {
      docker {
        image 'python:3.14-slim'
        args '-v $PWD:/app'
      }
    }

    environment {
        APP_NAME = "aceest_fitness"
        DOCKER_REPO = "yourdockerhubusername/aceest_fitness"
        PYTHON = "python3"
        KUBE_CONFIG_ID = "kube-config"
        SONARQUBE_SERVER = "SonarQubeServer"
        DOCKER_CREDS = "dockerhub-creds"
        GIT_CREDENTIALS = "github-token"
    }

    // triggers {
    //     // Poll SCM every 5 minutes for changes
    //     pollSCM('H/5 * * * *')
    // }

    stages {
        stage('Clean Workspace') {
            steps {
                // Clean checkout
                cleanWs()
            }
        }

        stage('Setup Python Environment') {
            steps {
                echo "🔹 Setting up virtual environment and installing dependencies..."
                sh """
                ${PYTHON} -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt pytest pytest-flask
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "🧪 Running Pytest test cases..."
                sh """
                . venv/bin/activate
                mkdir -p reports
                pytest -v --disable-warnings --junitxml=reports/pytest-results.xml
                """
            }
            post {
                always {
                    junit 'reports/pytest-results.xml'
                }
            }
        }

        // stage('SonarQube Analysis') {
        //     steps {
        //         echo "🔍 Running SonarQube static code analysis..."
        //         withSonarQubeEnv("${SONARQUBE_SERVER}") {
        //             sh """
        //             sonar-scanner \
        //             -Dsonar.projectKey=ACEest_Fitness \
        //             -Dsonar.sources=. \
        //             -Dsonar.host.url=$SONAR_HOST_URL \
        //             -Dsonar.login=$SONAR_AUTH_TOKEN
        //             """
        //         }
        //     }
        // }

        // stage('Build Docker Image') {
        //     steps {
        //         echo "🐳 Building Docker image..."
        //         sh """
        //         VERSION=$(git describe --tags --always || echo latest)
        //         docker build -t ${DOCKER_REPO}:$VERSION .
        //         docker tag ${DOCKER_REPO}:$VERSION ${DOCKER_REPO}:latest
        //         """
        //     }
        // }

        // stage('Push Docker Image') {
        //     steps {
        //         echo "📦 Pushing Docker image to Docker Hub..."
        //         withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDS}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
        //             sh """
        //             echo $PASS | docker login -u $USER --password-stdin
        //             VERSION=$(git describe --tags --always || echo latest)
        //             docker push ${DOCKER_REPO}:$VERSION
        //             docker push ${DOCKER_REPO}:latest
        //             """
        //         }
        //     }
        // }

        // stage('Deploy to Kubernetes') {
        //     steps {
        //         echo "🚀 Deploying updated app to Kubernetes cluster..."
        //         withCredentials([file(credentialsId: "${KUBE_CONFIG_ID}", variable: 'KUBECONFIG')]) {
        //             sh """
        //             kubectl apply -f deployment.yaml --kubeconfig $KUBECONFIG
        //             kubectl apply -f service.yaml --kubeconfig $KUBECONFIG
        //             kubectl rollout status deployment/aceest-fitness-deployment --kubeconfig $KUBECONFIG
        //             """
        //         }
        //     }
        // }

        // stage('Tag Build and Archive') {
        //     steps {
        //         echo "🏷️ Tagging Git version and archiving build artifact..."
        //         sh """
        //         VERSION=v$(date +'%Y.%m.%d.%H%M')
        //         git config user.email "jenkins@ci.local"
        //         git config user.name "Jenkins CI"
        //         git tag -a $VERSION -m "Automated build $VERSION"
        //         git push origin $VERSION || true

        //         mkdir -p build
        //         zip -r build/${APP_NAME}-$VERSION.zip .
        //         """
        //         archiveArtifacts artifacts: 'build/*.zip', fingerprint: true
        //     }
        // }
    }

    post {
        success {
            echo "✅ Build completed successfully!"
        }
        failure {
            echo "❌ Build failed. Please check console output for errors."
        }
    }
}
