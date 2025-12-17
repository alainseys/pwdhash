FROM python:3.11.13-bullseye

# Set the workspace enviroment variable Worspace
ENV WORKSPACE_BASE_PATH=/workspaces/ansible

# Copy the private key into the image
COPY ../private_key /workspaces/ansible/private_key
RUN chmod 600 /workspaces/ansible/private_key
RUN echo "eval \$(ssh-agent -s)" >> /etc/bash.bashrc && \
    echo "ssh-add /workspaces/ansible/private_key" >> /etc/bash.bashrc


# Install sshpass
#RUN apt-get update -y && \
#    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends sshpass

RUN echo 'SSHD: ALL' >> /etc/hosts.allow

# Upgrade pip and install necessary Python packages
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install ansible ansible-lint ansible-dev-tools ansible-builder ansible-creator ansible-navigator pywinrm molecule pyVmomi requests \
    docker netmiko yamllint dnspython pytest-molecule


# Set up bash aliases and environment variables
#RUN echo "alias ansible-update='git push origin HEAD:main'" >> /etc/bash.bashrc
#RUN echo "alias apply-template=${WORKSPACE_BASE_PATH}/scripts/copy-template.sh" >> /etc/bash.bashrc
#RUN echo "export ANSIBLE_CONFIG=${WORKSPACE_BASE_PATH}/ansible.cfg" >> /etc/bash.bashrc
#RUN echo "alias ansible-submodules='${WORKSPACE_BASE_PATH}/scripts/ansible-submodules.sh'" >> /etc/bash.bashrc


# Docker specs to use with molecule
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg-agent less software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Kerberos requirements
#RUN apt-get update && \ 
#    apt-get install gcc -y \
#    python3-dev \
#    libkrb5-dev \
#    gss-ntlmssp
RUN git config --global user.email "alain.seys@outlook.com"
RUN git config --global user.name "Alain Seys"
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Change Back to correct workdir
WORKDIR ${WORKSPACE_BASE_PATH}
