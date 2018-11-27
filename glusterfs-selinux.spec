%global selinuxtype targeted
%global moduletype contrib
%global modulename glusterd
%global selinux_policyver POLICY_VERSION


Name:		glusterfs-selinux
Version:	0.1.0
Release:	2%{?dist}
Summary:	Glusterfs targeted SELinux policy

License:	GPLv2
URL:		https://github.com/gluster/glusterfs-selinux
Source0:	%{name}-%{version}.tar.gz

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


%description
SELinux targeted policy modules for glusterfs


%prep
%setup -q -n %{name}-%{version}


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
%attr(0644,root,root) %{_datadir}/selinux/packages/%{modulename}.pp.bz2
%attr(0644,root,root) %{_datadir}/selinux/devel/include/contrib/%{modulename}.if
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}



%changelog
* Thu Nov 15 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-2
- corrections toward review request comments from misc - bz#1649713

* Mon Jul 02 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-1
- first build

