import { Box, Flex, Button, Spacer, Link } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <Box bg="gray.800" p={4} color="white">
      <Flex maxW="1200px" mx="auto" align="center">
        <Link href="/" fontSize="xl" fontWeight="bold">
          Investa
        </Link>
        <Spacer />
        <Button onClick={() => navigate("/login")} colorScheme="blue" mr={2}>
          登入
        </Button>
        <Button onClick={() => navigate("/register")} colorScheme="green">
          註冊
        </Button>
      </Flex>
    </Box>
  );
};

export default Navbar;