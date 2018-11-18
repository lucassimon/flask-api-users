pipeline {
    environment {
        MONGODB_URI_TEST = credentials('MONGO_DB_TEST')
        FLASK_ENV = 'testing'
        FLASK_APP = 'application.py'
        DEBUG = true
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
        stage('Envs') {
            steps('Print Env After source checkout') {

                echo "Branch Name: ${env.BRANCH_NAME}"
                echo "BUILD_NUMBER : ${env.BUILD_NUMBER}"
                echo "BUILD_ID : ${env.BUILD_ID}"
                echo "JOB_NAME: ${env.JOB_NAME}"
                echo "BUILD_TAG : ${env.BUILD_TAG}"
                echo "EXECUTOR_NUMBER : ${env.EXECUTOR_NUMBER}"
                echo "NODE_NAME: ${env.NODE_NAME}"
                echo "NODE_LABELS : ${env.NODE_LABELS}"
                echo "WORKSPACE : ${env.WORKSPACE}"
                echo "JENKINS_HOME : ${env.JENKINS_HOME}"

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
        stage('Generate Release') {
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
                    sh """make release v=${releaseInput}"""
                }
            }
        }
        stage('Deploy stage') {
            steps {
                echo 'Deploy master to stage'
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
