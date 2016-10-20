package selenium.tests;

import static org.junit.Assert.*;

import java.util.List;

import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import io.github.bonigarcia.wdm.ChromeDriverManager;


public class PullTestLarge {
	private static WebDriver driver;
	
	@BeforeClass
	public static void setUp() throws Exception 
	{
		//driver = new HtmlUnitDriver();
		ChromeDriverManager.getInstance().setup();
		driver = new ChromeDriver();
	}
	
	@AfterClass
	public static void  tearDown() throws Exception
	{
		driver.close();
		driver.quit();
	}
	
	@Test
	public void testCrabot() throws Exception
	{
		
	       driver.get("https://github.com/login");
	       WebElement id = driver.findElement(By.xpath("//input[@id='login_field']"));
	       WebElement pass = driver.findElement(By.xpath("//input[@id='password']"));
	       WebElement button = driver.findElement(By.xpath("//input[@value='Sign in']"));        

	       id.sendKeys("KakanotCollaborator");
	       pass.sendKeys(System.getenv("KAKAPWD"));
	       button.submit();
	       WebDriverWait wait = new WebDriverWait(driver, 30);
	       int i = 7;
	       String patchNo = "patch-38";
	       driver.get("https://github.com/KakanotCollaborator/Repo1");
	       wait.until(ExpectedConditions.visibilityOfAllElementsLocatedBy(By.xpath("//div[2]/div[1]/div[4]/a")));
	       WebElement PR1 = driver.findElement(By.xpath("//div[2]/div[1]/div[4]/a"));

	       if(PR1 != null)
	       {

	    	   PR1.click();
	    	   driver.get("https://github.com/codekaka/Repo1/compare/master...KakanotCollaborator:master");
	    	   WebElement listBranches = driver.findElement(By.xpath("//div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/button/span"));
	    	   Thread.sleep(1000);
	   		   listBranches.click();
	    	   wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div/div[3]/div[1]/a["+i+"]/div")));
	    	   WebElement branchLatest = driver.findElement(By.xpath("//div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div/div[3]/div[1]/a["+i+"]/div"));
	    	   Thread.sleep(1000);
	    	   branchLatest.click();
	   		   driver.get("https://github.com/codekaka/Repo1/compare/master...KakanotCollaborator-"+patchNo);	
	    	   WebElement PR2 = driver.findElement(By.xpath("//div[2]/div[1]/div[2]/div/button"));
	    	   Thread.sleep(1000);
	    	   PR2.click();

	    	   //WebElement PR3 = driver.findElement(By.xpath("//div[2]/div/div/div[3]/button"));
	    	   //Thread.sleep(10000);
	    	   //PR3.click();
	    	   Thread.sleep(2000);
	    	   List <WebElement> btns = driver.findElements(By.xpath("//button[@class='btn btn-primary']"));
	   		
		   		final String COMMENT_STR = "Create pull request";
		   		for(WebElement btn : btns) {
		   			if(COMMENT_STR.equalsIgnoreCase(btn.getText())) {
		   				btn.submit();
		   			}
		       }
		   		Thread.sleep(15000);	//wait for crabot to comment.
				
				WebElement lastCommentATag = driver.findElement(By.xpath("//div[@class='timeline-comment-wrapper js-comment-container'][last()]/a"));		
				assertNotNull(lastCommentATag);
				
				final String codeKakaUserURL = "https://github.com/codekaka";
				assertEquals(codeKakaUserURL, lastCommentATag.getAttribute("href"));
				
				String commentText = "Testing happy case for large commit size: @codekaka Run S1,S3";
				commentOnPR(commentText);
				Thread.sleep(15000);	//wait for crabot to comment.
				
				lastCommentATag = driver.findElement(By.xpath("//div[@class='timeline-comment-wrapper js-comment-container'][last()]/a"));		
				assertNotNull(lastCommentATag);
				
				assertEquals(codeKakaUserURL, lastCommentATag.getAttribute("href"));
				
				commentText = "Testing alternative case for large commit size: @codekaka Run all";
				commentOnPR(commentText);
				Thread.sleep(15000);	//wait for crabot to comment.
				
				lastCommentATag = driver.findElement(By.xpath("//div[@class='timeline-comment-wrapper js-comment-container'][last()]/a"));		
				assertNotNull(lastCommentATag);
				
				assertEquals(codeKakaUserURL, lastCommentATag.getAttribute("href"));
	       }
	}
	
	public void commentOnPR(final String commentText) throws Exception
	{		
		// http://geekswithblogs.net/Aligned/archive/2014/10/16/selenium-and-timing-issues.aspx
		WebDriverWait wait = new WebDriverWait(driver, 60);
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//textarea[@id='new_comment_field']")));
		WebElement textArea = driver.findElement(By.xpath("//textarea[@id='new_comment_field']"));		
		textArea.sendKeys(commentText);
		
		List <WebElement> btns = driver.findElements(By.xpath("//button[@class='btn btn-primary']"));
		final String COMMENT_STR = "Comment";
		for(WebElement btn : btns) {
			if(COMMENT_STR.equalsIgnoreCase(btn.getText())) {
				btn.submit();
			}
		}
	}

}
