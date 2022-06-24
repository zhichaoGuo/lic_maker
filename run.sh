docker pull [your Harbpr path]/lic_maker/lic_maker:0.1
docker run -p 80:80 -v `pwd`/database:/home/lic_maker/database -v `pwd`/log:/home/lic_maker/log [your Harbpr path]/lic_maker/lic_maker:0.1