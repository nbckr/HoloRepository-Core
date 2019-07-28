import React, { Component } from "react";
import { Router } from "@reach/router";
import AppContainer from "../app/core/AppContainer";
import PublicContainer from "../public/PublicContainer";
import AboutPage from "../public/AboutPage";
import LandingPage from "../public/LandingPage";
import ErrorPage from "../public/ErrorPage";
import DeviceConnectorPage from "../app/DeviceConnectorPage";
import HologramsListPage from "../app/holograms/HologramsListPage";
import PatientListPage from "../app/patients/PatientListPage";
import PatientDetailPage from "../app/patient/PatientDetailPage";
import ProfileInformationPage from "../app/ProfileInformationPage";
import NewHologramPage from "../app/new_hologram/NewHologramPage";

class MainContainer extends Component {
  render() {
    return (
      <>
        <Router>
          <PublicContainer path="/">
            <LandingPage default path="start" />
            <AboutPage path="about" />
          </PublicContainer>

          <AppContainer path="app">
            <PatientListPage path="patients" />
            <PatientDetailPage path="patient/:pid" />
            <DeviceConnectorPage path="devices" />
            <HologramsListPage path="holograms" />
            <NewHologramPage path="holograms/new" />
            <ProfileInformationPage path="profile" />
            <ErrorPage default />
          </AppContainer>
        </Router>
      </>
    );
  }
}

export default MainContainer;
