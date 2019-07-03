FROM puckel/docker-airflow


# Please change the enviroment variable based on vertica version
# VERTICA_9_0_1='9.0.1-4'
# VERTICA_9_1_1='9.1.1-0'
# VERTICA_9_2_0='9.2.0-0'
ENV AIRFLOW_HOME=/usr/local/airflow \
  VERTICA_DOMAIN='https://www.vertica.com/client_drivers' \
  VERTICA_DRIVER='9.1.1-0' \
  TIMEZONE="Asia/Dubai"

USER root
WORKDIR /

RUN apt-get update -yqq && apt-get install git wget awscli -yqq && \
  mkdir -p "${AIRFLOW_HOME}/.ssh" && \
  mkdir -p "${AIRFLOW_HOME}/config" && \
  touch "${AIRFLOW_HOME}/.ssh/known_hosts" && \
  mkdir -p "$AIRFLOW_HOME/git" && \
  mkdir -p "${AIRFLOW_HOME}"/airflowScripts && \
  ssh-keyscan -p 443 github.com >> "$AIRFLOW_HOME/.ssh/known_hosts" && \
  ssh-keyscan -p 443 ssh.github.com >> "$AIRFLOW_HOME/.ssh/known_hosts"

COPY ./git_ssh_config "${AIRFLOW_HOME}"/.ssh/config

# update timezone (use @ in sed because timezone contains /)
RUN ln -sf /usr/share/zoneinfo/${TIMEZONE} /etc/localtime && \
    sed -i "s@\(default_timezone\).*@\1 = ${TIMEZONE}@" /usr/local/airflow/airflow.cfg

# kerberos
ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -y krb5-user libpam-krb5 libpam-ccreds && \
  mkdir -p /etc/security/keytabs && \
  touch /etc/security/keytabs/etl.keytab && \
  chown airflow:airflow /etc/security/keytabs/etl.keytab  && \
  mkdir -p /etc/krb5.conf.d
ENV KRB5_CONFIG="${AIRFLOW_HOME}/config/kerberos/krb5.conf"

# Vertica
RUN export VS_SHORT=$(echo ${VERTICA_DRIVER} | cut -d . -f -2).x && \
  export V_NAME=vertica-client-${VERTICA_DRIVER}.x86_64.tar.gz && \
  export V_URI=${VERTICA_DOMAIN}/${VS_SHORT}/${VERTICA_DRIVER}/${V_NAME} && \
  printf "Downloading ${V_URI} @ /tmp/${V_NAME} \n" && \
  wget -q -O /tmp/${V_NAME} ${V_URI} && \
  tar vzxf /tmp/${V_NAME} -C / && \
  rm -rf /tmp/${V_NAME}

RUN chown -R airflow:airflow /opt/vertica/ && \
  apt-get -y install unixodbc unixodbc-dev && \
  printf "[Driver]\nDriverManagerEncoding=UTF-16" > "${AIRFLOW_HOME}/.vertica.ini"

# etl config
RUN mkdir -p $AIRFLOW_HOME/infa_config

# extra requirements
COPY ./requirements.txt /requirements.txt
RUN /bin/su - airflow -c "$(which pip) install --user -r /requirements.txt" && \
    /bin/su - airflow -c "$(which pip3) install --user -r /requirements.txt"

COPY src/airflowScripts "${AIRFLOW_HOME}/airflowScripts/"
COPY ./entrypoint.sh "/entrypoint.sh"
RUN chmod +x /entrypoint.sh && \
  chmod +x "${AIRFLOW_HOME}"/airflowScripts/*.sh && \
  chown -R airflow:airflow "$AIRFLOW_HOME"

USER airflow
WORKDIR ${AIRFLOW_HOME}

# bash
RUN echo "alias ll='ls -ltra'" >> .bashrc

# environment config
ENV PYTHONPATH=${PYTHONPATH:+${PYTHONPATH}:}"${AIRFLOW_HOME}/python/:${AIRFLOW_HOME}/"
ENV VERTICAINI="${AIRFLOW_HOME}/.vertica.ini"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
