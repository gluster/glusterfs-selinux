%global selinuxtype targeted
%global moduletype contrib
%global modulename glusterd


Name:		glusterfs-selinux
Version:	0.1.0
Release:	2%{?dist}
Summary:	Glusterfs targeted SELinux policy

License:	GPLv2
URL:		https://github.com/gluster/glusterfs-selinux
Source0:	%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
Requires:       selinux-policy-targeted
Requires(post): selinux-policy-targeted
BuildRequires:  pkgconfig(systemd)
BuildRequires:  selinux-policy-devel
Requires(post): selinux-policy-targeted
Requires(post): libselinux-utils
Requires(post): policycoreutils
%{?selinux_requires}


%description
SELinux targeted policy modules for glusterfs


%prep
%setup -q -n %{name}-%{version}


%build
make %{?_smp_mflags}


%install
%make_install


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
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/%{moduletype}/ipp-%{modulename}.if
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}



%changelog
* Thu May 07 2020 Vit Mojzis <vmojzis@redhat.com> - 0.1.0-2
- Update based on DSP guidelines
  https://fedoraproject.org/wiki/SELinux/IndependentPolicy

* Thu Nov 15 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-2
- corrections toward review request comments from misc - bz#1649713

* Mon Jul 02 2018 Milind Changire <mchangir@redhat.com> - 0.1.0-1
- first build

