pipeline {
  agent any
  triggers {
      cron('H 8,12,17 * * 1-5')
    }
  options {
    buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
    timeout(time: 30, unit: 'MINUTES')
    timestamps()
  }
  stages {
    stage('Tests') {
        steps {
            script{
                docker.image('msk-docker-hub01.ti.ru/python3allure').inside("-v $WORKSPACE:/usr/src/app -w /usr/src/app") { c ->
                sh 'pytest -vv -l --junit-xml=junit.xml --alluredir=allure_reports'
              }
            }
          }
    }
  }
  post {
    always {
      junit 'junit.xml'
	  script {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'allure_reports']]
                ])
      }
    }
  }
}
