%global selinuxtype targeted
%global moduletype contrib
%global modulename glusterfs
%global selinux_policyver POLICY_VERSION


Name:		glusterfs-selinux
Version:	0.1.0
Release:	1%{?dist}
Summary:	Glusterfs selinux policy

License:	GPLv2
URL:		https://github.com/gluster/glusterfs-selinux
Source0:	glusterfs-selinux.tar.gz

BuildArch:      noarch
BuildRequires:	git
Requires:	selinux-policy >= %{selinux_policyver}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): libselinux-utils
Requires(post): policycoreutils
%if 0%{?fedora}
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
SELinux targeted policy modules for glusterfs.


%prep
%setup -q -n %{name}.git


%build
make %{?_smp_mflags}


%install
install -d %{buildroot}%{_datadir}/selinux/packages
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
%make_install


%pre
%selinux_relabel_pre -s %{selinuxtype}


%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{modulename}.pp.bz2


%postun
if [ $1 -eq 0 ]; then
        %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi


%posttrans
%selinux_relabel_post -s %{selinuxtype}


%files
%defattr(-,root,root,0755)
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/contrib/glusterd.if
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{selinuxmodulename}



%changelog
* Mon Jul 02 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-1
- first build

