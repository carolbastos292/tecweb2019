import React from "react";
import { Route, Switch } from "react-router-dom";
// reactstrap components
import { Container } from "reactstrap";
// core components
import Sidebar from "components/Admin/Sidebar/Sidebar.jsx";

import AdminFooter from "components/Admin/Footers/AdminFooter.jsx";

import routes from "routes.js";

class Permissoes extends React.Component {
  componentDidUpdate(e) {
    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    //this.refs.mainContent.scrollTop = 0;
  }
  getRoutes = routes => {
    return routes.map((prop, key) => {
      if (prop.layout === "/permissoes") {
        return (
          <Route
            path={prop.layout + prop.path}
            component={prop.component}
            key={key}
          />
        );
      } else {
        return null;
      }
    });
  };
  getBrandText = path => {
    for (let i = 0; i < routes.length; i++) {
      if (
        this.props.location.pathname.indexOf(
          routes[i].layout + routes[i].path
        ) !== -1
      ) {
        return routes[i].name;
      }
    }
    return "Brand";
  };
  render() {
    return (
      <>
        <Sidebar
          {...this.props}
          routes={routes}
          logo={{
            innerLink: "/admin/index",
            imgSrc: require("assets/img/brand/argon-react.png"),
            imgAlt: "..."
          }}
        />
        <div className="main-content" ref="mainContent">
        <Switch>{this.getRoutes(routes)}</Switch>
        <Container>
          <AdminFooter />
      </Container>
      </div>
      </>
    );
  }
}

export default Permissoes;