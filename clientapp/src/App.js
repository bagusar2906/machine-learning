import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Nav, NavItem, NavLink } from "reactstrap";
import CommandForm from "./components/CommandForm"; // Import CommandForm component
import ChatUI from "./components/ChatUI"; // Placeholder for another form

const App = () => {
    const [activeTab, setActiveTab] = useState("command");

    return (
        <Container fluid>
            <Row>
                {/* Sidebar */}
                <Col md={3} className="bg-dark text-white vh-100 p-3">
                    <h4 className="text-center">Menu</h4>
                    <Nav vertical>
                        <NavItem>
                            <NavLink href="#" className={`nav-link ${activeTab === "command" ? "text-warning" : "text-white"}`} onClick={() => setActiveTab("command")}>
                                📜 Train Robot
                            </NavLink>
                        </NavItem>
                        <NavItem>
                            <NavLink href="#" className={`nav-link ${activeTab === "another" ? "text-warning" : "text-white"}`} onClick={() => setActiveTab("another")}>
                                📝 Inference
                            </NavLink>
                        </NavItem>
                    </Nav>
                </Col>

                {/* Main Content */}
                <Col md={9} className="p-4">
                    {activeTab === "command" && <CommandForm />}
                    {activeTab === "another" && <ChatUI />}
                </Col>
            </Row>
        </Container>
    );
};

export default App;
