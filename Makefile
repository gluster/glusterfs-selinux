TARGET?=glusterd
MODULES?=${TARGET:=.pp.bz2}
SHAREDIR?=/usr/share
SELINUXTYPE?=targeted

VERSION = 0.1.0
PACKAGE = glusterfs-selinux
distdir = $(PACKAGE)-$(VERSION)
DIST_TARGETS = dist-gzip

am__remove_distdir = \
  if test -d "$(distdir)"; then \
    find "$(distdir)" -type d ! -perm -200 -exec chmod u+w {} ';' \
      && rm -rf "$(distdir)" \
      || { sleep 5 && rm -rf "$(distdir)"; }; \
  else :; fi


all: ${TARGET:=.pp.bz2}

%.pp.bz2: %.pp
	@echo Compressing $^ -\> $@
	bzip2 -9 $^

%.pp: %.te
	make -f ${SHAREDIR}/selinux/devel/Makefile $@

clean:
	rm -f *~  *.tc *.pp *.pp.bz2
	rm -rf tmp *.tar.gz

man: install-policy
	sepolicy manpage --path . --domain ${TARGET}_t

install-policy: all
	semodule -i ${TARGET}.pp.bz2

install:
	install -D -m 644 ${TARGET}.pp.bz2 ${DESTDIR}${SHAREDIR}/selinux/packages/${SELINUXTYPE}/${TARGET}.pp.bz2
#	install -D -p -m 644 ${TARGET}.if ${DESTDIR}${SHAREDIR}/selinux/devel/include/contrib/ipp-${TARGET}.if
#	install -D -m 644 ${TARGET}_selinux.8 ${DESTDIR}${SHAREDIR}/man/man8/

am__tar = $${TAR-tar} chof - "$$tardir"

distdir: $(DISTFILES)
	$(am__remove_distdir)
	test -d "$(distdir)" || mkdir "$(distdir)"
	test -f "$(distdir)/glusterd.fc" || cp -p glusterd.fc "$(distdir)/glusterd.fc"
	test -f "$(distdir)/glusterd.if" || cp -p glusterd.if "$(distdir)/glusterd.if"
	test -f "$(distdir)/glusterd.te" || cp -p glusterd.te "$(distdir)/glusterd.te"
	test -f "$(distdir)/Makefile" || cp -p  Makefile "$(distdir)/Makefile"

dist-gzip: distdir
	tardir=$(distdir) && $(am__tar) | eval GZIP= gzip $(GZIP_ENV) -c >$(distdir).tar.gz
	$(am__remove_distdir)

dist dist-all:
	$(MAKE) $(AM_MAKEFLAGS) $(DIST_TARGETS) am__post_remove_distdir='@:'
	$(am__remove_distdir)

prep:
	$(MAKE) dist;
	-mkdir -p rpmbuild/BUILD
	-mkdir -p rpmbuild/SPECS
	-mkdir -p rpmbuild/RPMS
	-mkdir -p rpmbuild/SRPMS
	-mkdir -p rpmbuild/SOURCES
	-rm -rf rpmbuild/SOURCES/*
	cp *.tar.gz ./rpmbuild/SOURCES
	cp glusterfs-selinux.spec ./rpmbuild/SPECS

srcrpm:
	rpmbuild --define '_topdir $(shell pwd)/rpmbuild' -bs rpmbuild/SPECS/glusterfs-selinux.spec
	mv rpmbuild/SRPMS/* .

rpms:
	rpmbuild --define '_topdir $(shell pwd)/rpmbuild' -bb rpmbuild/SPECS/glusterfs-selinux.spec
	mv rpmbuild/RPMS/*/* .
