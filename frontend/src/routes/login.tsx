import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  Divider,
  FormControl,
  FormErrorMessage,
  HStack,
  Icon,
  Image,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Text,
  VStack,
  useBoolean,
} from "@chakra-ui/react";
import { FaGoogle, FaApple } from "react-icons/fa";
import { Link as RouterLink, createFileRoute, redirect } from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";
import Logo from "/assets/images/Invest.jpg";
import type { Body_login_login_access_token as AccessToken } from "../client";
import useAuth, { isLoggedIn } from "../hooks/useAuth";
import { emailPattern } from "../utils";

export const Route = createFileRoute("/login")({
  component: AuthPage,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" });
    }
  },
});

function AuthPage() {
  const [isLogin, setIsLogin] = useBoolean(true);
  
  const [show, setShow] = useBoolean();
  const { loginMutation, error, resetError } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AccessToken>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    if (isSubmitting) return;
    resetError();
    try {
      await loginMutation.mutateAsync(data);
    } catch {
      // error is handled by useAuth hook
    }
  };

  return (
    <Container as="form" onSubmit={handleSubmit(onSubmit)} maxW="md" py={8}>
      <VStack spacing={4} align="stretch">
        <Image src={Logo} alt="FastAPI logo" height="auto" maxW="2xs" alignSelf="center" mb={4} />

        <Button leftIcon={<FaGoogle />} colorScheme="gray" variant="outline" w="full">
          Continue with Google
        </Button>
        <Button leftIcon={<FaApple />} colorScheme="gray" variant="outline" w="full">
          Continue with Apple
        </Button>

        <HStack spacing={2} align="center" my={4}>
          <Divider />
          <Text fontSize="sm" whiteSpace="nowrap">or</Text>
          <Divider />
        </HStack>

        <FormControl isInvalid={!!errors.username || !!error}>
          <Input
            {...register("username", { required: "Email is required", pattern: emailPattern })}
            placeholder="Enter email address"
            type="email"
          />
          {errors.username && <FormErrorMessage>{errors.username.message}</FormErrorMessage>}
        </FormControl>

        <FormControl isInvalid={!!error}>
          <InputGroup>
            <Input
              {...register("password", { required: "Password is required" })}
              type={show ? "text" : "password"}
              placeholder="Password"
            />
            <InputRightElement>
              <Icon as={show ? ViewOffIcon : ViewIcon} onClick={setShow.toggle} cursor="pointer" />
            </InputRightElement>
          </InputGroup>
          {error && <FormErrorMessage>{error}</FormErrorMessage>}
        </FormControl>

        <Button type="submit" colorScheme="orange" w="full" isLoading={isSubmitting}>
          {isLogin ? "Log In" : "Create Free Account"}
        </Button>

        <Text fontSize="sm" align="center">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <Link color="blue.500" onClick={setIsLogin.toggle} cursor="pointer">
            {isLogin ? "Sign up" : "Log in"}
          </Link>
        </Text>

        <Text fontSize="xs" align="center" color="gray.500">
          By creating an account using any of the options above, you agree to the
          <Link color="blue.500" as={RouterLink} to="/terms"> Terms of Use </Link> &
          <Link color="blue.500" as={RouterLink} to="/privacy"> Privacy Policy</Link>
        </Text>
      </VStack>
    </Container>
  );
}
