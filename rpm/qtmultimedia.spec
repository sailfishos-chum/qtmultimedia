%global qt_version 5.15.8

%global openal 1
%global gst 1.0

Summary: Qt5 - Multimedia support
Name:    opt-qt5-qtmultimedia
Version: 5.15.8
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

# filter plugin/qml provides
%global __provides_exclude_from ^(%{_opt_qt5_archdatadir}/qml/.*\\.so|%{_opt_qt5_plugindir}/.*\\.so)$
%{?opt_qt5_default_filter}

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gstreamer-%{gst})
BuildRequires: pkgconfig(gstreamer-app-%{gst})
BuildRequires: pkgconfig(gstreamer-audio-%{gst})
BuildRequires: pkgconfig(gstreamer-base-%{gst})
BuildRequires: pkgconfig(gstreamer-pbutils-%{gst})
BuildRequires: pkgconfig(gstreamer-plugins-bad-%{gst})
BuildRequires: pkgconfig(gstreamer-video-%{gst})
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%if 0%{?openal}
BuildRequires: pkgconfig(openal)
%endif
# workaround missing dep
# /usr/include/gstreamer-1.0/gst/gl/wayland/gstgldisplay_wayland.h:26:10: fatal error: wayland-client.h: No such file or directory
BuildRequires: wayland-devel
Requires: opt-qt5-qtbase-gui >= %{qt_version}
Requires: opt-qt5-qtdeclarative >= %{qt_version}

%description
The Qt Multimedia module provides a rich feature set that enables you to
easily take advantage of a platforms multimedia capabilites and hardware.
This ranges from the playback and recording of audio and video content to
the use of available devices like cameras and radios.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
Requires: opt-qt5-qtdeclarative-devel%{?_isa}
# Qt5Multimedia.pc containts:
# Libs.private: ... -lpulse-mainloop-glib -lpulse -lglib-2.0
Requires: pkgconfig(libpulse-mainloop-glib)
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5} \
  CONFIG+=git_build \
  GST_VERSION=%{gst}

# have to restart build several times due to bug in sb2
%make_build  -k || chmod -R ugo+r . || true
%make_build

%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in *.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.*
%{_opt_qt5_libdir}/libQt5Multimedia.so.5*
%{_opt_qt5_libdir}/libQt5MultimediaQuick.so.5*
%{_opt_qt5_libdir}/libQt5MultimediaWidgets.so.5*
%{_opt_qt5_libdir}/libQt5MultimediaGstTools.so.5*
%if 0%{?openal}
%{_opt_qt5_archdatadir}/qml/QtAudioEngine/
%endif
%{_opt_qt5_archdatadir}/qml/QtMultimedia/
%{_opt_qt5_plugindir}/audio/
%{_opt_qt5_plugindir}/mediaservice/
%{_opt_qt5_plugindir}/playlistformats/
%dir %{_opt_qt5_libdir}/cmake/Qt5Multimedia/
%{_opt_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_*Plugin.cmake
%dir %{_opt_qt5_libdir}/cmake/Qt5MultimediaWidgets/
%{_opt_qt5_plugindir}/video/videonode/libeglvideonode.so

%files devel
%{_opt_qt5_headerdir}/QtMultimedia/
%{_opt_qt5_headerdir}/QtMultimediaQuick/
%{_opt_qt5_headerdir}/QtMultimediaWidgets/
%{_opt_qt5_headerdir}/QtMultimediaGstTools/
%{_opt_qt5_libdir}/libQt5Multimedia.so
%{_opt_qt5_libdir}/libQt5Multimedia.prl
%{_opt_qt5_libdir}/libQt5MultimediaQuick.so
%{_opt_qt5_libdir}/libQt5MultimediaQuick.prl
%{_opt_qt5_libdir}/libQt5MultimediaWidgets.so
%{_opt_qt5_libdir}/libQt5MultimediaWidgets.prl
%{_opt_qt5_libdir}/libQt5MultimediaGstTools.so
%{_opt_qt5_libdir}/libQt5MultimediaGstTools.prl
%{_opt_qt5_libdir}/cmake/Qt5Multimedia/Qt5MultimediaConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5MultimediaWidgets/Qt5MultimediaWidgetsConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5MultimediaGstTools/Qt5MultimediaGstToolsConfig*.cmake
%{_opt_qt5_libdir}/cmake/Qt5MultimediaQuick/Qt5MultimediaQuickConfig*.cmake
%{_opt_qt5_libdir}/pkgconfig/Qt5Multimedia.pc
%{_opt_qt5_libdir}/pkgconfig/Qt5MultimediaWidgets.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/*.pri
%{_opt_qt5_libdir}/cmake/Qt5Multimedia/Qt5Multimedia_QSGVideoNodeFactory_EGL.cmake
