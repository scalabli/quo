#-------------------------------------------------------------------------------
#
# Dockerfile for building a development container.
#
#-------------------------------------------------------------------------------
FROM photon:3.0

# Build variables.
ARG APP_NAME
ARG APP_VERSION
ARG GIT_REF
ARG GIT_URL

ARG MAINTAINER=secretum.inc@pm.me

# Install everything under the install/ directory to the root of the image.
ADD install /

# Install the python and basic tools and perform cleanup tasks in a single RUN
# step to keep our image footprint as small as possible.
RUN tdnf update -y \
    && tdnf install -y \
    gcc \
    gzip \
    make \
    python3-devel \
    python3-pip \
    && pip3 install --upgrade pip \
    && pip install wheel setuptools \
    && pip install \
    coverage \
    sphinx \
    sphinx_rtd_theme \
    twine \
    && tdnf clean all \
    && rm -rf /var/cache/tdnf/* \
    && ln -s /usr/bin/python3 /usr/bin/python

# Install the framework in a separate layer as this is the part most likely to
# change between builds. This allows us to re-use the previous layers when we
# have to rebuild.
RUN cd /tmp/python \
    && python setup.py install \
    && rm -rf /tmp/*

# Add some hopefully useful labels.
#
# We use some standard Label Schema attributes defined at:
#     http://label-schema.org/rc1/
#
LABEL \
    maintainer="${MAINTAINER}" \
    org.label-schema.schema-version="1.0.0" \
    org.label-schema.name="${APP_NAME}" \
    org.label-schema.description="Just another rakish application framework" \
    org.label-schema.vcs-url="${GIT_URL}" \
    org.label-schema.vcs-ref="${GIT_REF}" \
    org.label-schema.version="${APP_VERSION}"

# Set the default command to print the motd which contains some helpful
# information on how to use the container.
CMD [ "/usr/bin/cat", "/etc/motd" ]
