#! /bin/bash
export JAVA_HOME=`/usr/libexec/java_home`
cat ant_tags.csv| while read line
  do
    hash=$(echo $line | cut -f1 -d' ')
    version=$(echo $line | cut -f2 -d' ')
    cd ant
    git checkout -f $hash
    sh build.sh
    cp ./build/lib/ant.jar ../../jars/ant/ant-$version.jar
    cd ..
  done
