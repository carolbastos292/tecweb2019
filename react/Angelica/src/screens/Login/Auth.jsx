import React from "react";



// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  Container,
  CardBody,
  FormGroup,
  Form,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Row,
  Col
} from "reactstrap";

class Auth extends React.Component {

    signIn = () => {
        let formdata = new FormData();
        formdata.append('cpf',this.cpf);
        formdata.append('senha',this.senha);

        console.log(formdata);

        const requestInfo = {
            method: 'POST',
            body: formdata,
        };

        fetch('/autenticar', requestInfo)
            .then(response => {
                if(response.ok) {
                    console.log(response);
                    return response.json()
                }
                throw new Error("Login inválido...");
            })
            .then(token => {
                localStorage.setItem('token', token);
                this.props.history.push("/admin");
                return;
            })
            .catch(e => {
                this.setState({ message: e.message });
            });

    }

  render() {
    return (
      <> 
      <Container>
        <div className="header-body text-center mb-2">
          <Row className="justify-content-center">
            <Col lg="5" md="6">
              <h1 className="text-white">Angélica</h1>
              <p className="text-lead text-light">
                Sistema de Gerenciamento de Táxi
              </p>
            </Col>
          </Row>
        </div>
      </Container>
        <Col lg="5" md="7">
          <Card className="bg-secondary shadow border-0">
            <CardBody className="px-lg-5 py-lg-5">
              <div className="text-center text-muted mb-4">
                <small>Insira suas credenciais</small>
              </div>
              <Form role="form">
                <FormGroup className="mb-2">
                  <InputGroup className="input-group-alternative">
                    <InputGroupAddon addonType="prepend">
                      <InputGroupText>
                        <i className="ni ni-single-02" />
                      </InputGroupText>
                    </InputGroupAddon>
                    <Input  placeholder="CPF" type="CPF" id="cpf" onChange={e => this.cpf = e.target.value}  />
                  </InputGroup>
                </FormGroup>
                <FormGroup>
                  <InputGroup className="input-group-alternative">
                    <InputGroupAddon addonType="prepend">
                      <InputGroupText>
                        <i className="ni ni-lock-circle-open" />
                      </InputGroupText>
                    </InputGroupAddon>
                    <Input id="senha" placeholder="Senha" type="password" onChange={e => this.senha = e.target.value} />
                  </InputGroup>
                </FormGroup>
                <div className="custom-control custom-control-alternative custom-checkbox">
                  <input
                    className="custom-control-input"
                    id=" customCheckLogin"
                    type="checkbox"
                  />
                  <label
                    className="custom-control-label"
                    htmlFor=" customCheckLogin"
                  >
                    <span className="text-muted">Permanecer Conectado</span>
                  </label>
                </div>
                <div className="text-center">
                  <Button className="my-4" color="primary" block onClick={this.signIn}  type="button">
                    Entrar
                  </Button>
                </div>
              </Form>
            </CardBody>
          </Card>
          <Row className="mt-3">
           {/* <Col xs="6">
              <a
                className="text-light"
                href="#pablo"
                onClick={e => e.preventDefault()}
              >
                <small>Forgot password?</small>
              </a>
            </Col>
            <Col className="text-right" xs="6">
              <a
                className="text-light"
                href="#pablo"
                onClick={e => e.preventDefault()}
              >
                <small>Create new account</small>
              </a>
    </Col>*/}
          </Row>
        </Col>
      </>
    );
  }
}

export default Auth;