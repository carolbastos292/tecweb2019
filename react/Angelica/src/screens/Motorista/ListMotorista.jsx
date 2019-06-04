import React from "react";

// reactstrap components
import {
  Badge,
  Card,
  Button,
  CardHeader,
  CardFooter,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  DropdownToggle,
  Media,
  PaginationItem,
  PaginationLink,
  Progress,
  Table,
  Container,
  Row,
  Col,
  FormGroup,
  UncontrolledTooltip,
  InputGroupText,
  InputGroupAddon,
  InputGroup,
  Input,
} from "reactstrap";
// core components


import Header from "components/Login/Headers/UserHeader.jsx";
import Pagination from "components/Admin/Pagination/Pagination.jsx"

const customLabels = {

  first: '<<',
  last: '>>',
  previous: '<',
  next: '>'

};

const customStyle = {
  cursor: "Pointer"

};


class ListMotorista extends React.Component {

  constructor() {
    super();
    this.state = {
      motoristas: [],
      pageOfItems: []
    }
    this.onChangePage = this.onChangePage.bind(this)
    this.search = this.search.bind(this)
  }

  componentDidMount() {
    fetch('/drivers')
      .then(res => res.json())
      .then((data) => {
        this.setState({
          motoristas: data.data,
          pageOfItems: []
        })
        console.log(data);
      }

      )
      .catch(console.log)
  }

  onChangePage(pageOfItems) {
    // update state with new page of items
    this.setState({ pageOfItems: pageOfItems });
  }

  search(e){
    console.log(this.cpf)
  }

  render() {
    const motoristas = this.state.pageOfItems.map((item) =>
      <tr>
        <th scope="row">
          <Media className="align-items-center">
            <Media>
              <span className="mb-0 text-sm">
                {item.cpf}
              </span>
            </Media>
          </Media>
        </th>
        <td>{item.nome}</td>
        <td>{item.rg}</td>
        <td>{item.renach}</td>
        <td>{item.bairro}</td>
        <td>{item.rua}</td>
        <td>{item.cep}</td>
        <td>{item.telefone}</td>
        <td>{item.status}</td>
        <td>

          {
            item.status ? (
              <Badge color="primary" pill>
                Ativo
                              </Badge>

            ) : (
                <Badge color="danger" pill>
                  Inativo
                            </Badge>
              )}





        </td>
        <td className="text-right">
          <UncontrolledDropdown>
            <DropdownToggle
              className="btn-icon-only text-light"
              href="#pablo"
              role="button"
              size="sm"
              color=""
              onClick={e => e.preventDefault()}
            >
              <i className="fas fa-ellipsis-v" />
            </DropdownToggle>
            <DropdownMenu className="dropdown-menu-arrow" right>
              <DropdownItem
                href="#pablo"
                onClick={e => e.preventDefault()}
              >
                Editar
                            </DropdownItem>
              <DropdownItem
                href="#pablo"
                onClick={e => e.preventDefault()}
              >
                Excluir
                            </DropdownItem>
            </DropdownMenu>
          </UncontrolledDropdown>
        </td>
      </tr>
    )

    return (
      <>
     
        <Header />
        {/* Page content */}
        <Container className="mt--7" fluid>
          {/* Table */}
          <Row>
            <div className="col">
              <Card className="shadow">
                <CardHeader className="border-0">
                <Row>
                  <Col md="3">
                    <FormGroup>
                      <h3 className="mb-0">Buscar Motoristas</h3>
                    </FormGroup>
                  </Col>
                  <Col md="5">
                    <FormGroup>
                      <InputGroup className="input-group-alternative">
                      <Input placeholder="CPF" type="text" onChange={e => this.cpf = e.target.value}  />
                      <Button className="btn-icon btn-3" color="primary" type="button" onClick={this.search}>
                          Procurar
                        </Button>
                      </InputGroup>
                    </FormGroup>
                    
                  </Col>
                  <Col md="4">
                    <Button className="btn-icon btn-2" 
                          color="primary" 
                          type="button" 
                          className="float-right"
                          href="/motorista/add-motorista"
                    >
                          <span className="btn-inner--icon">
                            <i className="ni ni-fat-add" />
                          </span>
                    </Button>
                  </Col>
                </Row>
                </CardHeader>
                <Table className="align-items-center table-flush" responsive>
                  <thead className="thead-light">
                    <tr>
                      <th scope="col">CPF</th>
                      <th scope="col">NOME</th>
                      <th scope="col">RG</th>
                      <th scope="col">RENACH</th>
                      <th scope="col">BAIRRO</th>
                      <th scope="col">RUA</th>
                      <th scope="col">CEP</th>
                      <th scope="col">TELEFONE</th>
                      <th scope="col">STATUS</th>
                      <th scope="col" className="text-right">AÇÃO</th>
                      <th scope="col" />
                    </tr>
                  </thead>
                  <tbody>
                      {motoristas}
                  </tbody>
                </Table>
                <CardFooter>
                 <Pagination items={this.state.motoristas} 
                              onChangePage={this.onChangePage} 
                              customStyle={customElements.style} 
                              customLabels={customLabels} />
                </CardFooter>
              </Card>
             

            </div>
          </Row>
        </Container>
      </>
    );
  }
}

export default ListMotorista;