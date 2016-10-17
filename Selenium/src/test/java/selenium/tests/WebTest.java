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

public class WebTest2
{
	private static WebDriver driver;
	
	@BeforeClass
	public static void setUp() throws Exception 
	{
		//driver = new HtmlUnitDriver();
		ChromeDriverManager.getInstance().setup();
		//driver = new ChromeDriver();
		driver = new FirefoxDriver();		
		login();
	}
	
	@AfterClass
	public static void tearDown() throws Exception
	{
		driver.close();
		driver.quit();
	}
	
	public void commentOnPR() throws Exception
	{		
		// http://geekswithblogs.net/Aligned/archive/2014/10/16/selenium-and-timing-issues.aspx
		WebDriverWait wait = new WebDriverWait(driver, 60);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//textarea[@id='new_comment_field']")));
		WebElement textArea = driver.findElement(By.xpath("//textarea[@id='new_comment_field']"));			
		textArea.sendKeys("@codekaka can you analyze this?");
		
		List <WebElement> btns = driver.findElements(By.xpath("//button[@class='btn btn-primary']"));
		final String COMMENT_STR = "Comment";
		for(WebElement btn : btns) {
			if(COMMENT_STR.equalsIgnoreCase(btn.getText())) {
				btn.submit();
			}
		}
	}
	
	@Test
	public void verifyCrabotComment() throws Exception
	{
		driver.get("https://github.com/codekaka/Repo1/pull/3");
		commentOnPR();
		Thread.sleep(10000);	//wait for crabot to comment.
		
		WebElement lastCommentATag = driver.findElement(By.xpath("//div[@class='timeline-comment-wrapper js-comment-container'][last()]/a"));		
		assertNotNull(lastCommentATag);
		
		final String codeKakaUserURL = "https://github.com/codekaka";
		assertEquals(codeKakaUserURL, lastCommentATag.getAttribute("href"));
	}
	@Test
	public void CreatePR() throws Exception
	{
		
	       WebDriverWait wait = new WebDriverWait(driver, 30);
	       driver.get("https://github.com/codekaka/Repo1");
	       WebElement pullReq = driver.findElement(By.xpath("//div[2]/div[1]/div[3]/div/div/div/a"));
	       if(pullReq != null){
	    	   pullReq.click();
	    	   WebElement nxtScreenPullRequest = driver.findElement(By.xpath("//*[@id='new_pull_request']/div[2]/div/div/div[3]/button"));
	    	   nxtScreenPullRequest.click();
	    	   
	       }
	}
	
	public static void login() {
        driver.get("https://github.com/login");
        WebElement id = driver.findElement(By.xpath("//input[@id='login_field']"));
        WebElement pass = driver.findElement(By.xpath("//input[@id='password']"));
        WebElement button = driver.findElement(By.xpath("//input[@value='Sign in']"));         

        id.sendKeys("testcodekaka");
        pass.sendKeys("codekaka123");
        button.submit();
    }

}

