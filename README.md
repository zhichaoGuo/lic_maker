## 开发端
- 构建docker image

    ```bash
    docker build . -t lic_maker:0.1
    ```

- 标记docker image

    ```bash
    docker tag lic_server:0.1 [your Harbpr path]/lic_maker/lic_maker:0.1
    ```

- 推送docker image

    ```bash
    docker push [your Harbpr path]/lic_maker/lic_maker:0.1
    ```

- 运行本地docker image -> CONTAINER
    ```bash
    docker run -p 80:80 -v `pwd`/database:/home/lic_maker/database -v `pwd`/log:/home/lic_maker/log lic_maker:0.1
    ```
## 服务器端
- 拉取docker image

    ```bash
    docker pull [your Harbpr path]/lic_maker/lic_maker:0.1
    ```

- 运行拉取到的docker image -> CONTAINER
    ```bash
    docker run -p 80:80 -v `pwd`/database:/home/lic_maker/database -v `pwd`/log:/home/lic_maker/log [your Harbpr path]/lic_maker/lic_maker:0.1
    ```
- 使用脚本拉取并运行
    ```bash
    bash run.sh
    ```
