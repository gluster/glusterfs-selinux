%global selinuxtype targeted
%global moduletype contrib
%global modulename glusterd


Name:		glusterfs-selinux
Version:	0.1.1
Release:	4%{?dist}
Summary:	Glusterfs targeted SELinux policy

License:	GPLv2
URL:		https://github.com/gluster/glusterfs-selinux
Source0:	%{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}


%description
SELinux targeted policy modules for glusterfs


%prep
%setup -q -n %{name}-%{version}


%build
make %{?_smp_mflags}


%install
%make_install
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 8
	install -D -p -m 644 ${TARGET}.if ${DESTDIR}${SHAREDIR}/selinux/devel/include/contrib/ipp-${TARGET}.if
%endif



%pre
%selinux_relabel_pre -s %{selinuxtype}


%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2


%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi


%posttrans
%selinux_relabel_post -s %{selinuxtype}


%files
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 8
	%{_datadir}/selinux/devel/include/%{moduletype}/ipp-%{modulename}.if
%endif
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %attr(700, root, root) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license COPYING


%changelog
* Wed Jan 27 2021 Rinku Kothiya <rkothiya@redhat.com> - 0.1.1-4
- Incorporated review comments - bz#1901123

* Thu May 07 2020 Vit Mojzis <vmojzis@redhat.com> - 0.1.0-3
- Update based on DSP guidelines
  https://fedoraproject.org/wiki/SELinux/IndependentPolicy

* Thu Nov 15 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-2
- corrections toward review request comments from misc - bz#1649713

* Mon Jul 02 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-1
- first build

