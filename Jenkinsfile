pipeline {
    environment {
        MONGODB_URI_TEST = credentials('API_USERS_MONGO_DB_TEST')
        FLASK_ENV = 'testing'
        FLASK_APP = 'application.py'
        DEBUG = true
        HOSTS = credentials('API_USERS_DEPLOY_HOSTS')
	}
    options
    {
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '3', daysToKeepStr: '7'))
        timestamps()
    }
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage ("Install Dependencies") {
            steps {
                sh """
                python3 -m venv .venv
                source .venv/bin/activate
                pip install --upgrade pip
                pip install -r ${env.WORKSPACE}/requirements/test.txt
                """
            }
        }
        stage('Run Tests') {
            steps {
                sh """
                source .venv/bin/activate
                echo "Running the unit test..."
                make clean
                make coverage
                """
            }
        }
        stage('Generate Release and deploy') {
            steps {
                script {
                    def version = readFile encoding: 'utf-8', file: '__version__.py'
                    def message = "Latest ${version}. New version:"
                    def releaseInput = input(
                        id: 'userInput',
                        message: "${message}",
                        parameters: [
                            [
                                $class: 'TextParameterDefinition',
                                defaultValue: 'uat',
                                description: 'Release candidate',
                                name: 'rc'
                            ]
                        ]
                    )
                    sh """
                    make release v=${releaseInput}
                    source .venv/bin/activate
                    fab -H ${env.HOSTS} deploy --tag ${releaseInput}
                    """
                }
            }
        }
    }
    post {
        always {
            sh """
            rm -rf .venv
            """
        }
        success {
            echo "Success"
        }
        failure {
            echo "Send e-mail, when failed"
        }
    }
}
