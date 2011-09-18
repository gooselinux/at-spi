%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define atk_version 1.13.0
%define gtk2_version 2.10.0
%define gail_version 1.9.0
%define libbonobo_version 2.4.0
%define orbit2_version 2.6.0
%define pango_version 1.2.0

Summary: Assistive Technology Service Provider Interface
Name: at-spi
Version: 1.28.1
Release: 2%{?dist}
URL: http://developer.gnome.org/projects/gap/
Source0: http://download.gnome.org/sources/at-spi/1.28/%{name}-%{version}.tar.bz2

License: LGPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: gtk2 >= %{gtk2_version}
Requires: libbonobo >= %{libbonobo_version}
Requires: ORBit2 >= %{orbit2_version}
Requires: gail >= %{gail_version}
Requires: atk >= %{atk_version}

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: ORBit2-devel >= %{orbit2_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: dbus-glib-devel
BuildRequires: GConf2-devel
BuildRequires: fontconfig
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: libX11-devel
BuildRequires: libXtst-devel
BuildRequires: libXi-devel
BuildRequires: libXevie-devel
BuildRequires: libXt-devel
BuildRequires: gnome-common
BuildRequires: automake, autoconf, libtool, intltool

# http://bugzilla.gnome.org/show_bug.cgi?id=548782
Patch0: evo-crash.patch

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.


%package devel
Summary: Development files for at-spi
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: atk-devel >= %{atk_version}
Requires: gtk2-devel >= %{gtk2_version}
Requires: libbonobo-devel >= %{libbonobo_version}
Requires: ORBit2-devel >= %{orbit2_version}
Requires: gail-devel >= %{gail_version}
Requires: pkgconfig

%description devel
This package contains libraries, header files and developer documentation
needed for developing applications that interact directly with at-spi.


%package python
Summary: Python bindings for at-spi
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: python
Requires: pyorbit
Requires: gnome-python2-bonobo

%description python
This package contains Python bindings allowing to use at-spi in Python programs.


%prep
%setup -q
%patch0 -p1 -b .evo-crash

autoreconf -i -f

%build
%configure --disable-gtk-doc --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang at-spi

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la

mv $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version} \
   $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel-%{version}

%pre
if [ "$1" -gt 1 -a -f %{_sysconfdir}/gconf/schemas/at-spi.schemas ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/at-spi.schemas >& /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/at-spi.schemas >& /dev/null || :
fi

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/at-spi.schemas >& /dev/null || :


%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f at-spi.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_libdir}/lib*.so.*
%{_libdir}/bonobo/servers/*
%{_libdir}/orbit-2.0/*
%{_libdir}/gtk-2.0/modules/*
%{_libexecdir}/*
%{_sysconfdir}/gconf/schemas/at-spi.schemas
%{_sysconfdir}/xdg/autostart/at-spi-registryd.desktop

%files devel
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}-devel-%{version}
%{_datadir}/gtk-doc/html/*
%{_datadir}/idl/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files python
%defattr(-,root,root)
%{python_sitearch}/pyatspi/


%changelog
* Mon May  3 2010 Matthias Clasen <mclasen@redhat.com> - 1.28.1-2
- Add missing requires to the -python subpackage
Resolves: #586508

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 1.28.1-1
- Update to 1.28.1

* Fri Oct  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.28.0-3
- Fix an oversight in the previous patch that caused
  registryd to slow down logout by ~10 seconds

* Sun Sep 27 2009 Matthias Clasen <mclasen@redhat.com> - 1.28.0-2
- Use dbus sm api instead of xsmp, avoid segfault at logout (#519239)

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 1.28.0-1
- Update to 1.28.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 1.27.92-1
- Update to 2.27.92

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 1.27.91-1
- Update to 2.27.91

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.26.0-2
- Rebuild

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 1.26.0-1
- Update to 1.26.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.25.92-1
- Update to 1.25.92

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 1.25.5-1
- Update to 2.25.5

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 1.25.4-2
- Update to 1.25.4

* Wed Dec 10 2008 Matthias Clasen <mclasen@redhat.com> - 1.25.2-5
- ...but keep all the needed deps

* Mon Dec  8 2008 Matthias Clasen <mclasen@redhat.com> - 1.25.2-4
- Reduce unused direct deps 

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.25.2-3
- Rebuild for Python 2.6

* Tue Dec  2 2008 Matthias Clasen <mclasen@redhat.com> - 1.25.2-2
- Update to 1.25.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.25.1-3
- Rebuild for Python 2.6

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 1.25.1-2
- Tweak %%summary and %%description

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 1.25.1-1
- Update to 1.25.1

* Tue Oct 21 2008 Matthias Clasen <mclasen@redhat.com> - 1.24.0-5
- Prevent a crash in evo when changing components

* Fri Oct  3 2008 Matthias Clasen <mclasen@redhat.com> - 1.24.0-4
- Prevent at-spi module from being unloaded

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 1.24.0-2
- Update to 1.24.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.92-1
- Update to 1.23.92
- Drop upstreamed patch

* Fri Sep  5 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.91-3
- Fix an evo crash caused by the greeter crash fix

* Fri Sep  5 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.91-2
- Fix a greeter crash

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.91-1
- Update to 1.23.91

* Wed Aug 20 2008 Jarod Wilson <jarod@redhat.com> - 1.23.6-2
- Silence incessant atk-bridge spew filling xsession-errors (#459275)

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.6-1
- Update to 1.23.6

* Mon Jul 21 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.5-1
- Update to 1.23.5

* Tue Jun  3 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.3-1
- Update to 1.23.3

* Mon May  5 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.1-2
- Bump rev

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.1-1
- Update to 1.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Wed Mar  5 2008 Christopher Aillon <caillon@redhat.com> - 1.21-92-2
- Perf improvement work from Ginn Chen to help a11y-enabled-firefox3

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.92-1
- Update to 1.21.92

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.5-2
- Rebuild for gcc 4.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.5-1
- Update to 1.21.5

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.21.3-1
- Update to 1.21.3

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.21.1-1
- Update to 1.21.1

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 1.20.1-1
- Update to 1.20.1

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 1.20.0-1
- Update to 1.20.0

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.5-2
- Update license field

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.5-1
- Update to 1.19.5

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.3-1
- Update to 1.19.3
- Add a -python subpackage

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.1-1
- Update to 1.19.1

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.1-2
- Don't ship .la files

* Mon Apr  9 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.1-1
- Update to 1.18.1, which includes the previous patch
- Drop obsolete patch
- Fix a small memory leak

* Mon Mar 26 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.0-2
- Backport a patch to fix deadlocks in applications

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.0-1
- Update to 1.18.0
- Drop obsolete patch

* Thu Mar  8 2007 Ray Strode <rstrode@redhat.com> - 1.17.2-2
- add a patch that might fix some deadlock issues (bug 329454)

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.2-1
- Update to 1.17.2

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.1-1
- Update to 1.17.1

* Thu Feb 22 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.0-2
- Bump atk requirement

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.0-1
- Update to 1.17.0

* Wed Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 1.7.16-1
- Update to 1.7.16

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.7.15-1
- Update to 1.7.15

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.14-1
- Update to 1.7.14

* Sat Dec  9 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.13-2
- Small spec file cleanups

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.13-1
- Update to 1.7.13

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.12-1
- Update to 1.7.12

* Wed Aug 23 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.11-2.fc6
- Remove debug spew

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.11-1.fc6
- Update to 1.7.11
- Drop upstreamed patch
- Require pkgconfig in the -devel package

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.10-1.fc6
- Update to 1.7.10

* Fri Jul 28 2006 Alexander Larsson <alexl@redhat.com> - 1.7.9-3
- Fix segfault if a11y enabled on x86-64 (#196063)

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.9-2
- Rebuild

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.9-1
- Update to 1.7.9

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.8-1
- Update to 1.7.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.7.7-8.1
- rebuild

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.7-8
- Add a BuildRequires

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.7-7
- Make it build in mock

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.7-6
- Revert the previous change

* Tue Apr  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.7-5
- Fix a missing declaration
- Fix segfaults on x86_64

* Tue Apr  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.7-1
- Update to 1.7.7

* Thu Mar  9 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.6-2
- Fix a crash on x86_64

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.6-1
- Update to 1.7.6 

* Tue Feb 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.7.5-1
- Update to 1.7.5 

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.7.4-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.7.4-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> 1.7.4-1
- Update to 1.7.4

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> 1.7.3-1
- Update to 1.7.3

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> 1.7.2-1
- Update to 1.7.2

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 31 2005 Matthias Clasen <mclasen@redhat.com> 1.6.6-2
- Switch requires to modular X

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 1.6.6-1
- Update to 1.6.6

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuilt

* Tue Jun 28 2005 Matthias Clasen <mclasen@redhat.com> 1.6.4-1
- Update to 1.6.4

* Mon Mar 14 2005 Matthias Clasen <mclasen@redhat.com> 1.6.2-1
- Update to 1.6.3

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> 1.6.2-2
- Rebuilt with gcc4

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> 1.6.2-1
- Update to 1.6.2

* Wed Sep 29 2004 Elliot Lee <sopwith@redhat.com> 1.6.0-3
- Remove dependency on linc-devel

* Fri Sep 24 2004 Mark McLoughlin <markmc@redhat.com> 1.6.0-2
- Fix some random spec file issues (fixes #133430?)

* Thu Sep 23 2004 Jonathan Blandford <jrb@redhat.com> 1.6.0-1
- bump version

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 1.5.3-1
- Update to 1.5.3

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 1.4.0-1
- Update to 1.4.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 1.3.15
- Update to 1.3.15

* Thu Mar 04 2004 Mark McLoughlin <markmc@redhat.com> 1.3.14-1
- Update to 1.3.14

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 1.3.13-1
- update to 1.3.13

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 30 2004 Jonathan Blandford <jrb@redhat.com> 1.3.11-1
- new version

* Thu Oct  2 2003 Jonathan Blandford <jrb@redhat.com> 1.3.7-1
- new version

* Wed Aug 20 2003 Elliot Lee <sopwith@redhat.com> 1.1.9-3
- Fix rebuild failure (stderr.patch)

* Tue Jul 15 2003 Havoc Pennington <hp@redhat.com> 1.1.9-2
- disable gtk doc

* Mon Jul 14 2003 Havoc Pennington <hp@redhat.com>
- automated rebuild

* Mon Jul  7 2003 Havoc Pennington <hp@redhat.com> 1.1.9-1
- 1.1.9
- remove multilib patch fixed upstream

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 1.1.8-3
- kill Xft buildreq

* Tue Feb 11 2003 Havoc Pennington <hp@redhat.com> 1.1.8-2
- rebuild to fix self-dependency

* Tue Feb 11 2003 Havoc Pennington <hp@redhat.com> 1.1.8-1

- extend multilib patch to cover -lXi

* Tue Feb  4 2003 Havoc Pennington <hp@redhat.com> 1.1.8-1
- 1.1.8

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Elliot Lee <sopwith@redhat.com> 1.0.1-6
- Add patch to help multilib systems find libXtst

* Fri Dec  6 2002 Havoc Pennington <hp@redhat.com>
- rebuild

* Sat Jul 27 2002 Havoc Pennington <hp@redhat.com>
- rebuild with new libbonobo and gail

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Matt Wilson <msw@redhat.com>
- add libatk-bridge.so to the file list

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 1.0.1
- add at-spi-registryd to file list

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 1.0.0
- add post/postun ldconfig

* Wed May 29 2002 Bill Nottingham <notting@redhat.com>
- rebuild again?

* Tue May 28 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 28 2002 Havoc Pennington <hp@redhat.com>
- 0.12.1

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 0.0.6

* Mon Jan 28 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide, seems to have been linked incorrectly

* Thu Jan 24 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide, upgrade to 0.0.5
- add gail deps

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- Initial build.


