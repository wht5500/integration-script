def gitclone(max)
{
  for (int k = 0; k< max; k++)
  {
      echo "checkout section: $k"
      
  }

}

pipeline {
    agent none
    //agent any
    //agent {
    //    label 'sh_mcu'
       //node('sh_mcu')
   // }
    
    environment{
        LANG = "C.UTF-8"
        USER = "wanghaitao"
        
    }
    
    parameters{
        string(name:"BRANCH", defaultValue:"dev",description:"branch name")
    }
    
    options{
        ansiColor('xterm')
        timestamps()

    }
    

                
    stages {

        stage('clean') {
            steps {
                echo 'clean'
                //rm ***
                script {
                    for (int i = 0; i < 10; i++)
                    {
                        echo "check and remove files: section$i"
                        
                    }
                    
                }
            }

        }
        
        stage('checkout') {
            steps {
                echo 'sync'
                gitclone(7)
            }
        }
    

        stage('build') {
            failFast true
            parallel {
                stage('build mcu') {
                steps {
                    echo 'build'
                    sleep 60
                    }
                }
                stage('build qnx') {
                steps {
                    sleep 80
                    echo 'build'
                    }
                } 
                stage('build android') {
                steps {
                    sleep 100
                    echo 'build'
                    }
                } 
                
            }
            
        }
        stage('combine') {
            steps {
                echo 'combine'
            }
        }
        stage('test') {
            steps {
                echo 'test'
                //bat 'sonar-scan ****'
            }
        }
        stage('deploy') {
            steps {
                echo 'deploy'
                //bat 'lftp ********'
            }
        }
        
    }
    
    post{
        failure{
            mail to: '**@**.com', subject:'The pipeline failed', body:'see the detail ${env.BUILD_URL}%\n'
        }
        success{
            mail to: '**@**.com', subject:'The pipeline success', body:'good job\n'
        }
        
    }
    
}
