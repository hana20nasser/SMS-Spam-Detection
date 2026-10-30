FROM quay.io/jupyter/scipy-notebook:latest
USER root
RUN mkdir -p /home/jovyan/bd-a1 && chown -R ${NB_UID}:${NB_GID} /home/jovyan/bd-a1
USER ${NB_UID}
WORKDIR /home/jovyan/bd-a1
COPY --chown=${NB_UID}:${NB_GID} requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=${NB_UID}:${NB_GID} data/ ./data/
COPY --chown=${NB_UID}:${NB_GID} notebook/ ./notebook/
RUN mkdir -p output/figures screenshots
EXPOSE 8888
CMD ["start-notebook.py", "--ServerApp.root_dir=/home/jovyan/bd-a1", "--ServerApp.token=assignment1"]
