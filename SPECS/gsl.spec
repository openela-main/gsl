Summary: The GNU Scientific Library for numerical analysis
Name: gsl
Version: 2.5
Release: 1%{?dist}
URL: http://www.gnu.org/software/gsl/
# info part of this package is under GFDL license
# eigen/nonsymmv.c and eigen/schur.c
# contains rutiens which are part of LAPACK - under BSD style license
License: GPLv3 and GFDL and BSD
Group: System Environment/Libraries

Source: ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Patch0: gsl-1.10-lib64.patch
# http://lists.gnu.org/archive/html/bug-gsl/2015-12/msg00012.html
Patch1: gsl-tol.patch
Patch2: gsl-test.patch
BuildRequires: pkgconfig

%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.

%package devel
Summary: Libraries and the header files for GSL development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info 
Requires: pkgconfig, automake

%description devel
The gsl-devel package contains the header files necessary for 
developing programs using the GSL (GNU Scientific Library).

%prep
%setup -q
%patch0 -p1 -b .lib64
%patch1 -p1 -b .tol
%patch2 -p1 -b .test

iconv -f windows-1252 -t utf-8 THANKS  > THANKS.aux
touch -r THANKS THANKS.aux
mv THANKS.aux THANKS

%build
# disable FMA
%ifarch aarch64 ppc64 ppc64le s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -ffp-contract=off"
%endif
%configure
make %{?_smp_mflags}

%check
make check || ( cat */test-suite.log && exit 1 )

%install
make install DESTDIR=$RPM_BUILD_ROOT install='install -p'
# remove unpackaged files from the buildroot
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# remove static libraries
rm -r $RPM_BUILD_ROOT%{_libdir}/*.a


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gsl-ref.info.gz ]; then
    /sbin/install-info %{_infodir}/gsl-ref.info %{_infodir}/dir || :
fi

%preun devel
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/gsl-ref.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/gsl-ref.info %{_infodir}/dir || :
    fi
fi

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/libgsl.so.23*
%{_libdir}/libgslcblas.so.0*
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_mandir}/man1/gsl-histogram.1*
%{_mandir}/man1/gsl-randist.1*

%files devel
%{_bindir}/gsl-config*
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/*info*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gsl.pc
%{_mandir}/man1/gsl-config.1*
%{_mandir}/man3/*.3*

%changelog
* Mon Aug 13 2018 Pavel Cahyna <pcahyna@redhat.com> - 2.5-1
- Update to 2.5

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Arthur Mello <amello@redhat.com> - 2.4-1
- Update to 2.4

* Tue Feb 14 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2.3-1
- rebase to 2.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 10 2016 Than Ngo <than@redhat.com> - 2.1-4
- fix build failure on powerpc

* Fri Feb 26 2016 Dan Horák <dan[at]danny.cz> - 2.1-3
- Disable FMA also on ppc64(le) and s390(x)

* Tue Feb 23 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.1-2
- Disable FMA on AArch64 to lower precision so tests do not fail.

* Sun Feb 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.1-1
- Update to 2.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 08 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.16-16
- Drop linkage patch: libgsl should not link to libgslcblas,
  so that more efficient libraries can be used (BZ #1007058).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.16-13
- Add upstream patch which fixes FTBFS on aarch64

* Sat Feb 15 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.16-12
- Drop ATLAS linkage patch: by design, the CBLAS library must be
  defined at link time to allow use of more optimized implementations.
  (BZ #1007058).

* Tue Oct 1 2013 Orion Poplawski <orion@cora.nwra.com> - 1.16-11
- Update to 1.16
- Rebase atlas patch
- Drop upstreamed ode patch

* Sat Sep 21 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-10
- linked against atlas 3.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jan 30 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-8
- self test moved to %%check section

* Tue Jan 29 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-7
- run self-tests after build
- updated ode-initval2 to upstream revision 4788

* Mon Nov 19 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-6
- minor cleanup of gsl.spec

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Peter Schiffer <pschiffe@redhat.com> - 1.15-3
- resolves: #741138
  removed unnecessary Requires: atlas

* Mon May  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.15-2
- resolves: #695148
  link gsl against atlas package for blas operations

* Mon May  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.15-1
- update to 1.15

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.14-1
- update to 1.14
- Resolves: #560219
             Library not linked correctly

* Wed Mar  3 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.13-2
- remove the static subpackage

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 1.13-1
- update to 1.13

* Mon Aug 17 2009 Ivana Varekova <varekova@redhat.com> - 1.12-6
- fix preun and post scripts (#517568)

* Mon Aug 10 2009 Ivana Varekova <varekova@redhat.com> - 1.12-5
- fix installation with --excludedocs option (#515971)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 07 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.12-3
- Remove rpaths (fix BZ#487823).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ivana Varekova <varekova@redhat.com> - 1.12-1
- update to 1.12

* Tue Sep 16 2008 Ivana Varekova <varekova@redhat.com> - 1.11-4
- Resolves: #462369 - remove %%{_datadir}/aclocal
- add automake dependency

* Mon Jul 28 2008 Ivana Varekova <varekova@redhat.com> - 1.11-3
- add -fgnu89-inline flag to solve gcc4.3 problem 
  remove gcc43 patch

* Wed Jun 18 2008 Ivana Varekova <varekova@redhat.com> - 1.11-2
- Resolves: #451006
  programs build with gcc 4.3 based on gsl require -fgnu89-inline 

* Mon Jun 16 2008 Ivana Varekova <varekova@redhat.com> - 1.11-1
- update to 1.11

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.10-10
- Autorebuild for GCC 4.3

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1.10-9
- source file change
- spec cleanup

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1.10-8
- fix man-pages directories

* Tue Oct 30 2007 Ivana Varekova <varekova@redhat.com> - 1.10-7
- add man pages

* Fri Oct 26 2007 Ivana Varekova <varekova@redhat.com> - 1.10-6
- minor spec changes

* Thu Oct 25 2007 Ivana Varekova <varekova@redhat.com> - 1.10-5
- minor spec changes

* Wed Oct 24 2007 Ivana Varekova <varekova@redhat.com> - 1.10-4
- add pkgconfig dependency
- separate static libraries to -static subpackage
- fix gsl-config script - thanks Patrice Dumas

