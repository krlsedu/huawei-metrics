#!groovy
env.RELEASE_COMMIT = "1";
env.VERSION_NAME = "";
env.SERVICE_NAME = "csctracker_services_invest"
env.IMAGE_NAME = "csctracker-invest"
env.REPOSITORY_NAME = "CscTrackerInvest"

pipeline {
    agent none
    stages {
        stage('CheckBranch') {
            agent any
            steps {
                script {
                    result = sh(script: "git log -1 | grep 'Triggered Build'", returnStatus: true)
                    echo 'result ' + result
                    env.RELEASE_COMMIT = result == 0 ? '0' : '1'
                }
            }
        }
        stage('Notificar início de build') {
            agent any
            when {
                expression { env.RELEASE_COMMIT != '0' }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'csctracker_token', variable: 'token_csctracker')]) {
                        httpRequest acceptType: 'APPLICATION_JSON',
                                contentType: 'APPLICATION_JSON',
                                httpMode: 'POST', quiet: true,
                                requestBody: '''{
                                                       "app" : "Jenkins",
                                                       "text" : "New build on service ''' + env.SERVICE_NAME + ''' branch ''' + env.BRANCH_NAME + ''' started"
                                                    }''',
                                customHeaders: [[name: 'authorization', value: 'Bearer ' + env.token_csctracker]],
                                url: 'https://gtw.csctracker.com/notify-sync/message'
                    }
                }
            }
        }
        stage('Gerar versão') {
            agent any
            when {
                expression { env.RELEASE_COMMIT != '0' }
            }
            steps {
                script {
                    echo 'RELEASE_COMMIT ' + env.RELEASE_COMMIT
                    if (env.BRANCH_NAME == 'master') {
                        echo 'Master'
                        VERSION = VersionNumber(versionNumberString: '${BUILD_DATE_FORMATTED, "yy"}.${BUILD_WEEK,XX}.${BUILDS_THIS_WEEK,XXX}')
                    } else {
                        echo 'Dev'
                        VERSION = VersionNumber(versionNumberString: '${BUILD_DATE_FORMATTED, "yyyyMMdd"}.${BUILDS_TODAY,XX}.${BUILD_NUMBER,XXXXX}')
                        VERSION = VERSION + '-SNAPSHOT'
                    }

                    withCredentials([usernamePassword(credentialsId: 'gitHub', passwordVariable: 'password', usernameVariable: 'user')]) {
                        script {
                            echo "Creating a new tag"
                            sh 'git pull https://krlsedu:${password}@github.com/krlsedu/' + env.REPOSITORY_NAME + '.git HEAD:' + env.BRANCH_NAME
                            sh 'echo ' + VERSION + ' > version.txt'
                            if (env.BRANCH_NAME == 'master') {
                                sh "git add ."
                                sh "git config --global user.email 'krlsedu@gmail.com'"
                                sh "git config --global user.name 'Carlos Eduardo Duarte Schwalm'"
                                sh "git commit -m 'Triggered Build: " + VERSION + "'"
                                sh 'git push https://krlsedu:${password}@github.com/krlsedu/' + env.REPOSITORY_NAME + '.git HEAD:' + env.BRANCH_NAME
                            }
                        }
                    }
                    env.VERSION_NAME = VERSION
                }
            }
        }
        stage('Docker image') {
            agent any
            when {
                expression { env.RELEASE_COMMIT != '0' }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        sh 'docker build -t krlsedu/' + env.IMAGE_NAME + ':latest -t krlsedu/' + env.IMAGE_NAME + ':' + env.VERSION_NAME + ' .'
                    } else {
                        sh 'docker build -t krlsedu/' + env.IMAGE_NAME + ':SNAPSHOT -t krlsedu/' + env.IMAGE_NAME + ':' + env.VERSION_NAME + ' .'
                    }
                }
            }
        }
        stage('Docker Push') {
            agent any
            when {
                expression { env.RELEASE_COMMIT != '0' }
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerHub', passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
                        sh "docker login -u ${env.dockerHubUser} -p ${env.dockerHubPassword}"
                        if (env.BRANCH_NAME == 'master') {
                            sh 'docker push krlsedu/' + env.IMAGE_NAME
                        } else {
                            sh 'docker push krlsedu/' + env.IMAGE_NAME + ':SNAPSHOT'
                        }
                        sh 'docker push krlsedu/' + env.IMAGE_NAME + ':' + env.VERSION_NAME
                    }
                }
            }
        }

        stage('Service update') {
            agent any
            when {
                expression { env.RELEASE_COMMIT != '0' }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        withCredentials([string(credentialsId: 'csctracker_token', variable: 'token_csctracker')]) {
                            sh 'docker service update --image krlsedu/' + env.IMAGE_NAME + ':' + env.VERSION_NAME + ' ' + env.SERVICE_NAME
                            httpRequest acceptType: 'APPLICATION_JSON',
                                    contentType: 'APPLICATION_JSON',
                                    httpMode: 'POST', quiet: true,
                                    requestBody: '''{
                                                       "app" : "Jenkins",
                                                       "text" : "The service ''' + env.SERVICE_NAME + ''' has been successfully updated to version: ''' + env.VERSION_NAME + '''"
                                                    }''',
                                    customHeaders: [[name: 'authorization', value: 'Bearer ' + env.token_csctracker]],
                                    url: 'https://gtw.csctracker.com/notify-sync/message'
                        }
                    } else {
                        withCredentials([usernamePassword(credentialsId: 'developHost', passwordVariable: 'password', usernameVariable: 'user')]) {
                            script {
                                echo "Update remote"
                                def remote = [:]
                                remote.name = 'DevelopHost'
                                remote.host = env.DEVELOP_HOST_IP
                                remote.user = env.user
                                remote.port = 22
                                remote.password = env.password
                                remote.allowAnyHosts = true
                                sshCommand remote: remote, command: "docker service update --image krlsedu/" + env.IMAGE_NAME + ":" + env.VERSION_NAME + " " + env.SERVICE_NAME
                            }
                        }
                        withCredentials([string(credentialsId: 'csctracker_token', variable: 'token_csctracker')]) {
                            httpRequest acceptType: 'APPLICATION_JSON',
                                    contentType: 'APPLICATION_JSON',
                                    httpMode: 'POST', quiet: true,
                                    requestBody: '''{
                                                       "app" : "Jenkins",
                                                       "text" : "The develop ''' + env.SERVICE_NAME + ''' has been successfully updated to version: ''' + env.VERSION_NAME + '''"
                                                    }''',
                                    customHeaders: [[name: 'authorization', value: 'Bearer ' + env.token_csctracker]],
                                    url: 'https://gtw.csctracker.com/notify-sync/message'
                        }
                    }
                }
            }
        }

        stage('Notificar fim de build') {
            agent any
            when {
                expression { env.RELEASE_COMMIT != '0' }
            }
            steps {
                script {
                    withCredentials([string(credentialsId: 'csctracker_token', variable: 'token_csctracker')]) {
                        httpRequest acceptType: 'APPLICATION_JSON',
                                contentType: 'APPLICATION_JSON',
                                httpMode: 'POST', quiet: true,
                                requestBody: '''{
                                                       "app" : "Jenkins",
                                                       "text" : "Build on service ''' + env.SERVICE_NAME + ''' branch ''' + env.BRANCH_NAME + ''' finished"
                                                    }''',
                                customHeaders: [[name: 'authorization', value: 'Bearer ' + env.token_csctracker]],
                                url: 'https://gtw.csctracker.com/notify-sync/message'
                    }
                }
            }
        }
    }
}
