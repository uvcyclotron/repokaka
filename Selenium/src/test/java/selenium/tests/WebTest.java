package selenium.tests;

import static org.junit.Assert.*;

import java.io.File;
import java.util.List;

import org.junit.AfterClass;
//import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
//import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import io.github.bonigarcia.wdm.ChromeDriverManager;

public class WebTest
{
	private static WebDriver driver;
	
	@BeforeClass
	public static void setUp() throws Exception 
	{
		//driver = new HtmlUnitDriver();
		ChromeDriverManager.getInstance().setup();
		driver = new ChromeDriver();
		//driver = new FirefoxDriver();		
		login();
	}
	
	@AfterClass
	public static void tearDown() throws Exception
	{
		driver.close();
		driver.quit();
	}
		
	public void commentOnCommit(final String commentText) throws Exception
	{		
		// http://geekswithblogs.net/Aligned/archive/2014/10/16/selenium-and-timing-issues.aspx
		WebDriverWait wait = new WebDriverWait(driver, 60);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//textarea[@id='new_commit_comment_field']")));
		WebElement textArea = driver.findElement(By.xpath("//textarea[@id='new_commit_comment_field']"));		
		textArea.sendKeys(commentText);
		
		List <WebElement> btns = driver.findElements(By.xpath("//button[@class='btn btn-primary']"));
		
		final String COMMENT_STR = "Comment on this commit";
		for(WebElement btn : btns) {
			if(COMMENT_STR.equalsIgnoreCase(btn.getText())) {
				btn.submit();
			}
		}
	}
	
	@Test
	public void testCrabotCommentForCommitHappyCase() throws Exception
	{
		driver.get("https://github.com/codekaka/Repo1/commit/7b02468b900363b63df174ae6d60b29d3eeffade");
		String commentText = "Testing happy case for commit use-case (use-case 4): @codekaka Hey!";
		commentOnCommit(commentText);
		Thread.sleep(15000);	//wait for crabot to comment.
		
		WebElement lastCommentATag1 = driver.findElement(By.xpath("//div[@class='timeline-comment-wrapper js-comment-container'][last()]/a"));		
		assertNotNull(lastCommentATag1);
		
		final String codeKakaUserURL = "https://github.com/codekaka";
		assertEquals(codeKakaUserURL, lastCommentATag1.getAttribute("href"));
		
		commentText = "@codekaka Run all!";
		commentOnCommit(commentText);
		Thread.sleep(15000);	//wait for crabot to comment.
		
		WebElement lastCommentATag2 = driver.findElement(By.xpath("//div[@class='timeline-comment-wrapper js-comment-container'][last()]/a"));		
		assertNotNull(lastCommentATag2);
		
		assertEquals(codeKakaUserURL, lastCommentATag2.getAttribute("href"));
	}

	public static void login() {
        driver.get("https://github.com/login");
        WebElement id = driver.findElement(By.xpath("//input[@id='login_field']"));
        WebElement pass = driver.findElement(By.xpath("//input[@id='password']"));
        WebElement button = driver.findElement(By.xpath("//input[@value='Sign in']"));         

        id.sendKeys("testcodekaka");
        pass.sendKeys(System.getenv("KAKAPWD"));
        button.submit();
    }

}

