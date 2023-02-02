#!/bin/bash 

error_msg() {
     echo -e "\nExample: $0 for file in /root/paas22_3_0/test_image/*.tar; do ./push.sh $file "harbor.mwp-mavenir.com:9443/mwppaas"; done"
}

# Check input arguments
if [  $# -le 1 ]
then
     error_msg
     exit 1
fi

# Check if docker command is working or not
docker images > /dev/null 2>&1; rc=$?;
if [[ $rc != 0 ]]; then
     error_msg
     exit 1
fi

echo -e "\nLoading $1"

# Loading Image
LOAD_RESULT=$(docker load -i $1)
IMAGE=${LOAD_RESULT#*: }

# Tagging image with harbor repository name
if [ ! -z "$2/${IMAGE#*\/*\/}" ]; then
     docker tag $IMAGE $2/${IMAGE#*\/*\/}
     echo "Retagged $IMAGE to $2/${IMAGE#*\/*\/}"

     # Overwriting image to new image with harbor repo name
     IMAGE=$2/${IMAGE#*\/*\/}
fi

# Pushing image to harbor repository

echo -e "\nPushing $IMAGE"
docker push $IMAGE

# Result if docker push was successful or not
if [[ $rc != 0 ]]; then
     echo -e "\nERROR: Push failed, check if you can log in to registry or not"
     exit 1
fi


echo "Image push part done!"
exit 0


