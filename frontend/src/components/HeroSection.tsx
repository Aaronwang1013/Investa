import { Box, Heading, Text, Button, Image } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <Box textAlign="center" mt="10">
      <Heading>掌握市場趨勢，做出明智投資</Heading>
      <Text mt={4}>透過先進的金融數據與分析，提升你的投資策略。</Text>
      <Button onClick={() => navigate("/register")} mt={6} colorScheme="blue">
        立即開始
      </Button>
      <Image
        src="https://source.unsplash.com/1200x500/?stock-market,finance"
        alt="金融市場"
        mt={6}
        borderRadius="lg"
      />
    </Box>
  );
};

export default HeroSection;