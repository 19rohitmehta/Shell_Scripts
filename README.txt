

1. PAAS image tag push script (To tag and push all paas images to harbor in one go)

for image in <PATH of IMAGES/*.tar; do ./push.sh $image "HARBOR_REPO"; done

e.g. 

for image in /root/paas22_3_0/test_image/*.tar; do ./push.sh $image "harbor.mwp-mavenir.com/mwppaas"; done

2. Deploy paas script (To untar and deploy paas components prometheus, istio and traefik in one go)

./deploy_paas.sh <PATH of CHARTS> <HARBOR_REPO>

e.g.

./deploy_paas.sh "/root/paas/Charts" "harbor.mwp-mavenir.com"