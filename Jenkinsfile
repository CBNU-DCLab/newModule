podTemplate(label: 'docker-build', 
  containers: [
    containerTemplate(
      name: 'git',
      image: 'alpine/git',
      command: 'cat',
      ttyEnabled: true
    ),
    containerTemplate(
      name: 'docker',
      image: 'docker',
      command: 'cat',
      ttyEnabled: true
    ),
  ],
  volumes: [ 
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'), 
  ]
) {
    node('docker-build') {
        def dockerHubCred = 'test'
        def appImage
        
        stage('Checkout'){
            container('git'){
                checkout scm
            }
        }
        
        stage('Build'){
            container('docker'){
                script {
                    appImage = docker.build("jeongmin99/newmodule")
                }
            }
        }
        
       

        stage('Push'){
            container('docker'){
                script {
                    docker.withRegistry('https://registry.hub.docker.com', dockerHubCred){
                        appImage.push("${env.BUILD_NUMBER}")
                        appImage.push("latest")
                    }
                }
            }
        }

     stage('Deploying container to Kubernetes') {

        script {
          //kubernetesDeploy(configs: "/root/project/newModule/new-deployment.yaml","/root/project/newModulenew-service.yaml")
          def kubectlPath = "/usr/bin/kubectl"
          
          // Kubernetes에 배포하기 위한 kubectl 명령어 실행
          sh 'ssh root@113.198.137.208 ${kubectlPath} apply -f newModulenew-service.yaml'
        
      }
    }
    }
    
}
